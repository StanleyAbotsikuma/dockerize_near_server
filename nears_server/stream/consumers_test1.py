import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class messageConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.set_name = None
        self.name = None
        self.user = None
       
    def connect(self):
        self.name = self.scope['url_route']['kwargs']['name']
        self.set_name = f'chat_{self.name}'
        self.user = self.scope['user']
        #print(self.channel_name)
        
        self.accept()

        # join the room group

        async_to_sync(self.channel_layer.group_add)(
            self.set_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.set_name,
            self.channel_name,
        )
        

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # print(text_data_json)
        data = text_data_json['data']
        type_send = text_data_json['message_type']
        
        
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            "chat_display",
            {
                'type':'payload',
                'message_type': type_send,
                'data': data,
            }
        )
        

    def payload(self, event):
       data = event.get('data')
       message_type = event.get('message_type')

    # Get the channel name of the specific WebSocket connection you want to send the message to
       target_channel_name = 'chat_init'  # replace with your target channel name

    # Send the message to the target WebSocket connection using the channel layer
       self.channel_layer.send(
        target_channel_name,
        {
            'type': 'send.message',
            'data': data,
            'message_type': message_type
        })
