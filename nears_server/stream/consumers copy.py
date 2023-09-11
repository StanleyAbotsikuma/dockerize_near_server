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
        message = text_data_json['message']
        message_type = text_data_json['message_type']
        
        print(message)
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.set_name,
            {
                'type': 'payload',
                'message': message,
                "username":str(self.user),
                'message_type': message_type,
                'sender_channel_name': self.channel_name
            }
        )
        

    def payload(self, event):
        # if self.user.is_authenticated:
        #     print(self.user)
        #sending to every except sender
        if self.channel_name != event.get('sender_channel_name'):

            #send every thing
            # self.send(text_data=json.dumps(event))

            print(event)
            self.send(json.dumps({'type': 'websocket.send','message':event.get("message"),'message_type':event.get("message_type"),'username':event.get("username")}))

