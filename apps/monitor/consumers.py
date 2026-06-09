import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.utils import timezone

from apps.accounts.models import User


class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close(code=4001)
            return

        if not user.is_teamlead:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add('monitor', self.channel_name)
        await self.accept()

        snapshot = await self.get_snapshot()
        await self.send(text_data=json.dumps({
            'type': 'snapshot',
            'data': snapshot,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('monitor', self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        if data.get('type') == 'get_snapshot':
            snapshot = await self.get_snapshot()
            await self.send(text_data=json.dumps({
                'type': 'snapshot',
                'data': snapshot,
            }))

    async def monitor_update(self, event):
        snapshot = await self.get_snapshot()
        await self.send(text_data=json.dumps({
            'type': 'update',
            'event': event.get('event'),
            'data': snapshot,
        }))

    @database_sync_to_async
    def get_snapshot(self):
        threshold = settings.OVERDUE_THRESHOLD_MINUTES
        cutoff = timezone.now() - timezone.timedelta(minutes=threshold)

        chatters = (
            User.objects
            .filter(role=User.Role.CHATTER)
            .prefetch_related('chatter_dialogs')
        )

        result = []
        for chatter in chatters:
            dialogs = chatter.chatter_dialogs.all()
            overdue = [
                d for d in dialogs
                if d.fan_waiting_since and d.fan_waiting_since <= cutoff
            ]
            result.append({
                'id': chatter.id,
                'username': chatter.username,
                'is_online': chatter.is_online,
                'last_seen': (
                    chatter.last_seen.isoformat()
                    if chatter.last_seen
                    else None
                ),
                'dialogs_count': len(dialogs),
                'overdue_count': len(overdue),
                'overdue_dialogs': [
                    {
                        'id': d.id,
                        'fan_name': d.fan_name,
                        'waiting_minutes': round(
                            (
                                    timezone.now() - d.fan_waiting_since
                            ).total_seconds()
                            / 60,
                            1,
                        ),
                    }
                    for d in overdue
                ],
            })

        return result
