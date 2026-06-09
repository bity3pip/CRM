# CRM Chatter

Мини-модуль CRM для работы чатеров с фанами.

## Стек

- Backend: Django + DRF + Channels (WebSocket)
- Redis 7
- PostgreSQL 15
- Daphne (ASGI сервер)

## Запуск

### Docker (рекомендуется)

\```bash
docker-compose up --build
\```

- Backend API: http://localhost:8000
- Admin: http://localhost:8000/admin

### Локально

\```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
daphne -p 8000 config.asgi:application
\```

## Тестовые учётки

| Логин      | Пароль   | Роль   |
|------------|----------|--------|
| teamlead   | test1234 | Тимлид |
| chatter1   | test1234 | Чатер  |
| chatter2   | test1234 | Чатер  |
| chatter3   | test1234 | Чатер  |
| model_anna | test1234 | Модель |
| model_kate | test1234 | Модель |

## API

### REST

| Метод | URL                              | Описание                    |
|-------|----------------------------------|-----------------------------|
| POST  | /api/auth/login/                 | Получить JWT токен          |
| GET   | /api/dialogs/                    | Список диалогов чатера      |
| GET   | /api/dialogs/{id}/messages/      | История сообщений           |
| POST  | /api/dialogs/{id}/messages/send/ | Отправить сообщение         |
| POST  | /api/dialogs/{id}/fan-message/   | Симуляция сообщения от фана |
| POST  | /api/dialogs/{id}/read/          | Обнулить непрочитанные      |
| GET   | /api/monitor/chatters/           | Метрики чатеров (тимлид)    |

### WebSocket

| URL                                  | Описание         |
|--------------------------------------|------------------|
| ws://host/ws/dialogs/{id}/?token=JWT | Чатер — диалог   |
| ws://host/ws/monitor/?token=JWT      | Тимлид — монитор |

## Симуляция входящего сообщения от фана

\```bash
curl -X POST http://localhost:8000/api/dialogs/1/fan-message/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Привет!", "message_type": "text"}'
\```

## Порог просрочки

Настраивается через env:

\```env
OVERDUE_THRESHOLD_MINUTES=5
PRESENCE_GRACE_SECONDS=30
\```