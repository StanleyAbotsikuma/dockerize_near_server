"""
ASGI config for near_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""



import os
import django
from channels.auth import AuthMiddlewareStack  # new import
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import stream.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE',  'near_server.settings')

django.setup()
from .jwt_auth import TokenAuthMiddleware

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': TokenAuthMiddleware(  # new
        URLRouter(
            stream.routing.websocket_urlpatterns
        )
    ),  # new
})
