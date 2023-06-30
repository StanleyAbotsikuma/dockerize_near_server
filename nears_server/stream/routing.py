from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    #for test
    re_path(r'ws/test/(?P<name>\w+)/', consumers.messageConsumer.as_asgi()),
     #for messages
    re_path(r'ws/messages/(?P<name>\w+)/', consumers.messageConsumer.as_asgi()),
     #for tracking
    re_path(r'ws/tracking/(?P<name>\w+)/', consumers.messageConsumer.as_asgi()),
    #for calls
    re_path(r'ws/call/(?P<name>\w+)/', consumers.messageConsumer.as_asgi()),
    #agents
    re_path(r'ws/agents/', consumers.messageConsumer.as_asgi()),
]