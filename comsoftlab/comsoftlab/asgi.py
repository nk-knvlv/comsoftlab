from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from comsoftlab_app.routing import ws_urlpatterns

from django.core.asgi import get_asgi_application
from django.urls import path

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comsoftlab_app.settings')


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
    )
})
