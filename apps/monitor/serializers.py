from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from apps.accounts.models import User


class ChatterMetricSerializer(serializers.ModelSerializer):
    dialogs_count = serializers.SerializerMethodField()
    overdue_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username',
                  'is_online', 'last_seen',
                  'dialogs_count', 'overdue_count'
                  ]

    def get_dialogs_count(self, obj):
        return obj.chatter_dialogs.count()

    def get_overdue_count(self, obj):
        threshold = settings.OVERDUE_THRESHOLD_MINUTES
        cutoff = timezone.now() - timezone.timedelta(minutes=threshold)
        return obj.chatter_dialogs.filter(
            fan_waiting_since__isnull=False,
            fan_waiting_since__lte=cutoff,
        ).count()
