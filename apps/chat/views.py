from django.utils import timezone
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Dialog, Message
from .pagination import MessageCursorPagination
from .permissions import IsChatter, IsChatterOrTeamlead
from .serializers import DialogSerializer, MessageSerializer


class DialogListView(generics.ListAPIView):
    serializer_class = DialogSerializer
    permission_classes = [IsChatter]

    def get_queryset(self):
        return (
            Dialog.objects
            .filter(chatter=self.request.user)
            .select_related('model', 'chatter')
            .prefetch_related('messages')
        )


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = MessageCursorPagination
    permission_classes = [IsChatterOrTeamlead]

    def get_queryset(self):
        dialog_id = self.kwargs['dialog_id']
        user = self.request.user

        if user.is_chatter:
            qs = Dialog.objects.filter(id=dialog_id, chatter=user)
        else:
            qs = Dialog.objects.filter(id=dialog_id)

        if not qs.exists():
            return Message.objects.none()

        return Message.objects.filter(dialog_id=dialog_id)


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsChatter]

    def get_dialog(self):
        return Dialog.objects.get(
            id=self.kwargs['dialog_id'],
            chatter=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        try:
            dialog = self.get_dialog()
        except Dialog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            message = serializer.save(
                dialog=dialog,
                sender_type=Message.SenderType.CHATTER,
            )
            dialog.fan_waiting_since = None
            dialog.save(update_fields=['fan_waiting_since', 'updated_at'])

        return Response(MessageSerializer(message).data,
                        status=status.HTTP_201_CREATED
                        )


class FanMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            dialog = Dialog.objects.get(id=self.kwargs['dialog_id'])
        except Dialog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            message = serializer.save(
                dialog=dialog,
                sender_type=Message.SenderType.FAN,
            )
            if not dialog.fan_waiting_since:
                dialog.fan_waiting_since = timezone.now()
            dialog.unread_count += 1
            dialog.save(update_fields=['fan_waiting_since',
                                       'unread_count',
                                       'updated_at']
                        )

        channel_layer = get_channel_layer()
        message_data = MessageSerializer(message).data

        async_to_sync(channel_layer.group_send)(
            f'dialog_{dialog.id}',
            {
                'type': 'fan.message',
                'message': message_data,
            }
        )
        async_to_sync(channel_layer.group_send)(
            'monitor',
            {
                'type': 'monitor.update',
                'dialog_id': dialog.id,
                'event': 'fan_wrote',
            }
        )

        return Response(MessageSerializer(message).data,
                        status=status.HTTP_201_CREATED
                        )


@api_view(['POST'])
@permission_classes([IsChatter])
def read_dialog(request, dialog_id):
    try:
        dialog = Dialog.objects.get(id=dialog_id, chatter=request.user)
    except Dialog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    dialog.unread_count = 0
    dialog.save(update_fields=['unread_count'])

    return Response({'status': 'ok'})
