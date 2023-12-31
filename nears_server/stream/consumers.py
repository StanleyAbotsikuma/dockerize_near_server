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
        # print(self.user)
        
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
        receiver = text_data_json['receiver']
        type = text_data_json['type']
        data =text_data_json['data']
       
        
        
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.set_name,
            {
                'type':'payload',
                'message_type': type,
                'data': data,
                'receiver': receiver,
            }
        )
        

    def payload(self, event):
        # if self.user.is_authenticated:
        #     print(self.user)
        #sending to every except sender
        if self.channel_name != event.get('sender_channel_name'):
            self.send(json.dumps({'data':event.get("data"),'type':event.get("message_type"),'receiver':event.get("receiver")}))

