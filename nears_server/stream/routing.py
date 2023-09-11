from django.urls import re_path

from . import consumers,consumers_test1,consumers_test2,emergency,agents

websocket_urlpatterns = [
    #for test
    re_path(r'ws/test/(?P<name>\w+)/', consumers.messageConsumer.as_asgi()),
     #for messages
    re_path(r'ws/messages/(?P<name>\w+)/', consumers.messageConsumer.as_asgi()),
     #for tracking
    re_path(r'ws/tracking/(?P<name>\w+)/', consumers.messageConsumer.as_asgi()),
    #for calls
    re_path(r'ws/emergency/', emergency.emergencyConsumer.as_asgi()),
    #agents
    re_path(r'ws/agents/', agents.agentsConsumer.as_asgi()),
    
    
        #agents
    re_path(r'ws/understanding1/(?P<name>\w+)/', consumers_test1.messageConsumer.as_asgi()),
    re_path(r'ws/understanding2/(?P<name>\w+)/', consumers_test2.messageConsumer.as_asgi()),
]