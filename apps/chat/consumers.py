import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db import transaction

from .models import Dialog, Message
from .serializers import MessageSerializer
from apps.accounts.presence import set_user_online, set_user_offline



class DialogConsumer(AsyncWebsocketConsumer):
    """
    WebSocket для чатера.
    Подключение: ws://host/ws/dialogs/{dialog_id}/?token=<jwt>
    Группа: dialog_{dialog_id}
    """

    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close(code=4001)
            return

        self.dialog_id = self.scope['url_route']['kwargs']['dialog_id']
        self.group_name = f'dialog_{self.dialog_id}'

        has_access = await self.check_access(user, self.dialog_id)
        if not has_access:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await set_user_online(user.id)

        await self.channel_layer.group_send(
            'monitor',
            {
                'type': 'monitor.update',
                'event': 'presence',
                'user_id': user.id,
                'is_online': True,
            }
        )

        await self.mark_as_read(self.dialog_id)

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

        if hasattr(self, 'user_id'):
            await set_user_offline(self.user_id)

            await self.channel_layer.group_send(
                'monitor',
                {
                    'type': 'monitor.update',
                    'event': 'presence',
                    'user_id': self.user_id,
                    'is_online': False,
                }
            )

    async def receive(self, text_data):
        user = self.scope['user']

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_error('Invalid JSON')
            return

        message_type = data.get('message_type', 'text')
        content = data.get('content', '').strip()
        ppv_price = data.get('ppv_price')

        if not content:
            await self.send_error('Content is required')
            return

        if message_type == 'ppv' and not ppv_price:
            await self.send_error('ppv_price is required for PPV messages')
            return

        message = await self.save_chatter_message(
            dialog_id=self.dialog_id,
            content=content,
            message_type=message_type,
            ppv_price=ppv_price,
        )

        if message is None:
            await self.send_error('Dialog not found')
            return

        payload = await self.serialize_message(message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': payload,
            }
        )

        await self.channel_layer.group_send(
            'monitor',
            {
                'type': 'monitor.update',
                'dialog_id': int(self.dialog_id),
                'event': 'chatter_replied',
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
        }))

    async def fan_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'fan_message',
            'message': event['message'],
        }))


    async def send_error(self, detail):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'detail': detail,
        }))

    @database_sync_to_async
    def check_access(self, user, dialog_id):
        if user.is_teamlead:
            return Dialog.objects.filter(id=dialog_id).exists()
        return Dialog.objects.filter(id=dialog_id, chatter=user).exists()

    @database_sync_to_async
    def mark_as_read(self, dialog_id):
        Dialog.objects.filter(id=dialog_id).update(unread_count=0)

    @database_sync_to_async
    def save_chatter_message(self, dialog_id, content, message_type, ppv_price):
        try:
            with transaction.atomic():
                dialog = Dialog.objects.select_for_update().get(id=dialog_id)
                message = Message.objects.create(
                    dialog=dialog,
                    sender_type=Message.SenderType.CHATTER,
                    content=content,
                    message_type=message_type,
                    ppv_price=ppv_price if message_type == 'ppv' else None,
                )
                dialog.fan_waiting_since = None
                dialog.save(update_fields=['fan_waiting_since', 'updated_at'])
                return message
        except Dialog.DoesNotExist:
            return None

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data