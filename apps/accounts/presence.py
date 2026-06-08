from django.utils import timezone
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def set_user_online(user_id):
    User.objects.filter(id=user_id).update(
        is_online=True,
        last_seen=timezone.now(),
    )


@database_sync_to_async
def set_user_offline(user_id):
    User.objects.filter(id=user_id).update(
        is_online=False,
        last_seen=timezone.now(),
    )