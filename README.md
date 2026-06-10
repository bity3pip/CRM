# CRM Chatter

Мини-модуль CRM для работы чатеров с фанами.

## Стек

- **Backend**: Django + DRF + Channels (WebSocket)
- **Frontend**: Vue 3 (Composition API) + Pinia
- **Redis 7**
- **PostgreSQL 15**
- **Daphne** (ASGI сервер)
- **Nginx** (реверс-прокси)

## Запуск

### Docker 

```bash
docker-compose up --build
```

- Фронт: http://localhost
- Backend API: http://localhost/api/
- Admin: http://localhost/admin

## Тестовые учётки

| Логин | Пароль | Роль     |
|-------|--------|----------|
| teamlead | test1234 | Teamlead |
| chatter1 | test1234 | Chatter  |
| chatter2 | test1234 | Chatter  |
| chatter3 | test1234 | Chatter  |
| model_anna | test1234 | Model    |
| model_kate | test1234 | Model   |

## REST API

| Метод | URL | Роль | Описание |
|-------|-----|------|----------|
| POST | /api/auth/login/ | все | Получить JWT токен |
| GET | /api/auth/me/ | все | Текущий пользователь |
| GET | /api/dialogs/ | chatter | Список диалогов |
| GET | /api/dialogs/{id}/messages/ | chatter | История сообщений |
| POST | /api/dialogs/{id}/messages/send/ | chatter | Отправить сообщение |
| POST | /api/dialogs/{id}/fan-message/ | все | Симуляция сообщения от фана |
| POST | /api/dialogs/{id}/read/ | chatter | Обнулить непрочитанные |
| GET | /api/monitor/chatters/ | teamlead | Метрики чатеров |

## WebSocket

| URL | Роль | Описание |
|-----|------|----------|
| ws://host/ws/dialogs/{id}/?token=JWT | chatter | Диалог в реальном времени |
| ws://host/ws/monitor/?token=JWT | teamlead | Монитор в реальном времени |


## Симуляция входящего сообщения от фана

```bash
# Получить токен
TOKEN=$(curl -s -X POST http://localhost/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "chatter1", "password": "test1234"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")

# Отправить сообщение от фана
curl -X POST http://localhost/api/dialogs/1/fan-message/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Привет!", "message_type": "text"}'
```

## Настройка порогов

```env
OVERDUE_THRESHOLD_MINUTES=5   # кол-во минут чтобы диалог считался просроченым
PRESENCE_GRACE_SECONDS=30     # grace period для presence
```