from django.contrib import admin
from .models import Dialog, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    list_display = ['fan_name', 'model',
                    'chatter', 'unread_count',
                    'fan_waiting_since', 'updated_at'
                    ]
    list_filter = ['chatter', 'model']
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['dialog', 'sender_type',
                    'message_type', 'content',
                    'created_at'
                    ]
    list_filter = ['sender_type', 'message_type']
