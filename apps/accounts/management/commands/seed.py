from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import User
from apps.chat.models import Dialog, Message


class Command(BaseCommand):
    help = 'Seed database with test data'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=False).exists():
            self.stdout.write('Database already seeded, skipping')
            return
        self.stdout.write('Seeding database...')

        teamlead = User.objects.create_user(
            username='teamlead',
            password='test1234',
            role=User.Role.TEAMLEAD,
            first_name='Team',
            last_name='Lead',
        )
        self.stdout.write(f'  Created teamlead: {teamlead.username}')

        model1 = User.objects.create_user(
            username='model_anna',
            password='test1234',
            role=User.Role.MODEL,
            first_name='Anna',
        )
        model2 = User.objects.create_user(
            username='model_kate',
            password='test1234',
            role=User.Role.MODEL,
            first_name='Kate',
        )
        self.stdout.write(f'  Created models: {model1.username}, '
                          f'{model2.username}')

        chatter1 = User.objects.create_user(
            username='chatter1',
            password='test1234',
            role=User.Role.CHATTER,
            first_name='Chatter',
            last_name='One',
        )
        chatter2 = User.objects.create_user(
            username='chatter2',
            password='test1234',
            role=User.Role.CHATTER,
            first_name='Chatter',
            last_name='Two',
        )
        chatter3 = User.objects.create_user(
            username='chatter3',
            password='test1234',
            role=User.Role.CHATTER,
            first_name='Chatter',
            last_name='Three',
        )
        self.stdout.write(f'  Created chatters: {chatter1.username}, '
                          f'{chatter2.username}, {chatter3.username}')

        now = timezone.now()

        dialog1 = Dialog.objects.create(
            fan_name='Fan_Alex',
            model=model1,
            chatter=chatter1,
        )
        self._add_history(dialog1, [
            ('fan', 'Привет! Как дела?'),
            ('chatter', 'Всё отлично, спасибо! А у тебя?'),
            ('fan', 'Тоже хорошо. Что делаешь?'),
            ('chatter', 'Думаю о тебе 😊'),
            ('fan', 'Правда? Расскажи подробнее...'),
        ])
        dialog1.fan_waiting_since = now - timedelta(minutes=10)
        dialog1.unread_count = 1
        dialog1.save()

        dialog2 = Dialog.objects.create(
            fan_name='Fan_Mike',
            model=model2,
            chatter=chatter1,
        )
        self._add_history(dialog2, [
            ('fan', 'Hello!'),
            ('chatter', 'Hi there! How are you?'),
            ('fan', 'Great! Can we talk?'),
            ('chatter', 'Of course! I\'m all yours 💕'),
        ])

        dialog3 = Dialog.objects.create(
            fan_name='Fan_John',
            model=model1,
            chatter=chatter2,
        )
        self._add_history(dialog3, [
            ('fan', 'Привет красотка!'),
            ('chatter', 'Привет! Рада тебя видеть 😘'),
            ('fan', 'Скучал по тебе'),
            ('chatter', 'Я тоже! Где ты пропадал?'),
            ('fan', 'Работа... Можем поговорить?'),
        ])
        dialog3.fan_waiting_since = now - timedelta(minutes=2)
        dialog3.unread_count = 1
        dialog3.save()

        dialog4 = Dialog.objects.create(
            fan_name='Fan_David',
            model=model2,
            chatter=chatter2,
        )
        self._add_history(dialog4, [
            ('fan', 'Hey! Are you free?'),
            ('chatter', 'Always free for you 😊'),
        ])

        dialog5 = Dialog.objects.create(
            fan_name='Fan_Chris',
            model=model1,
            chatter=chatter3,
        )
        self._add_history(dialog5, [
            ('fan', 'Привет!'),
            ('chatter', 'Привет!'),
            ('fan', 'Ты здесь?'),
            ('fan', 'Куда пропала?'),
        ])
        dialog5.fan_waiting_since = now - timedelta(minutes=20)
        dialog5.unread_count = 2
        dialog5.save()

        self.stdout.write(self.style.SUCCESS('\nDone! Test accounts:'))
        self.stdout.write('  teamlead  / test1234  (role: teamlead)')
        self.stdout.write('  chatter1  / test1234  (role: chatter)')
        self.stdout.write('  chatter2  / test1234  (role: chatter)')
        self.stdout.write('  chatter3  / test1234  (role: chatter)')
        self.stdout.write('  model_anna / test1234 (role: model)')
        self.stdout.write('  model_kate / test1234 (role: model)')

    def _add_history(self, dialog, messages):
        now = timezone.now()
        for i, (sender, content) in enumerate(messages):
            Message.objects.create(
                dialog=dialog,
                sender_type=sender,
                content=content,
                created_at=now - timedelta(minutes=len(messages) - i),
                is_read=True,
            )
        dialog.updated_at = now
        dialog.save(update_fields=['updated_at'])
