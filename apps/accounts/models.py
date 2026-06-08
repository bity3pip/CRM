from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CHATTER = 'chatter', 'Chatter'
        TEAMLEAD = 'teamlead', 'Team Lead'
        MODEL = 'model', 'Model'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CHATTER,
    )
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} ({self.role})'

    @property
    def is_chatter(self):
        return self.role == self.Role.CHATTER

    @property
    def is_teamlead(self):
        return self.role == self.Role.TEAMLEAD

    @property
    def is_model(self):
        return self.role == self.Role.MODEL