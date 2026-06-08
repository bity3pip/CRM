from django.db import models
from django.conf import settings
from django.utils import timezone


class Dialog(models.Model):
    fan_name = models.CharField(max_length=100)
    model = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='model_dialogs',
        limit_choices_to={'role': 'model'},
    )
    chatter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chatter_dialogs',
        limit_choices_to={'role': 'chatter'},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fan_waiting_since = models.DateTimeField(null=True, blank=True)
    unread_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Dialog'
        verbose_name_plural = 'Dialogs'

    def __str__(self):
        return f'{self.fan_name} → {self.model.username} (chatter: {self.chatter.username})'

    @property
    def is_overdue(self):
        if not self.fan_waiting_since:
            return False
        threshold = settings.OVERDUE_THRESHOLD_MINUTES
        delta = timezone.now() - self.fan_waiting_since
        return delta.total_seconds() / 60 > threshold

    @property
    def waiting_minutes(self):
        if not self.fan_waiting_since:
            return None
        delta = timezone.now() - self.fan_waiting_since
        return round(delta.total_seconds() / 60, 1)


class Message(models.Model):
    class SenderType(models.TextChoices):
        FAN = 'fan', 'Fan'
        CHATTER = 'chatter', 'Chatter'

    class MessageType(models.TextChoices):
        TEXT = 'text', 'Text'
        PPV = 'ppv', 'PPV'

    dialog = models.ForeignKey(
        Dialog,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender_type = models.CharField(max_length=10, choices=SenderType.choices)
    content = models.TextField()
    message_type = models.CharField(
        max_length=10,
        choices=MessageType.choices,
        default=MessageType.TEXT,
    )
    ppv_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'[{self.sender_type}] {self.dialog} — {self.content[:40]}'