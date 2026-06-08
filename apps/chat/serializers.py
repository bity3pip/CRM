from rest_framework import serializers
from .models import Dialog, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender_type', 'message_type', 'content', 'ppv_price', 'created_at', 'is_read']
        read_only_fields = ['id', 'sender_type', 'created_at', 'is_read']

    def validate(self, attrs):
        if attrs.get('message_type') == Message.MessageType.PPV:
            if not attrs.get('ppv_price'):
                raise serializers.ValidationError({'ppv_price': 'Required for PPV messages.'})
        return attrs


class DialogSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    model_username = serializers.CharField(source='model.username', read_only=True)

    class Meta:
        model = Dialog
        fields = [
            'id', 'fan_name', 'model_username',
            'unread_count', 'fan_waiting_since',
            'is_overdue', 'waiting_minutes',
            'updated_at', 'last_message',
        ]

    def get_last_message(self, obj):
        msg = obj.messages.last()
        if msg:
            return MessageSerializer(msg).data
        return None