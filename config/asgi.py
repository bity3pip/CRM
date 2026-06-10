import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import (  # noqa: E402
    AllowedHostsOriginValidator)  # noqa: E402
from apps.chat.middleware import JWTAuthMiddleware  # noqa: E402
from apps.chat.routing import (   # noqa: E402
    websocket_urlpatterns as chat_ws)  # noqa: E402
from apps.monitor.routing import (   # noqa: E402
    websocket_urlpatterns as monitor_ws)  # noqa: E402


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(JWTAuthMiddleware(
        URLRouter(chat_ws + monitor_ws)
    )
    ),
})
