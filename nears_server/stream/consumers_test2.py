import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class messageConsumer(AsyncWebsocketConsumer):
    async def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.set_name = None
        self.name = None
        self.user = None
       
    async def connect(self):
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

    async def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.set_name,
            self.channel_name,
        )
        

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        data = text_data_json['data']
        type_send = text_data_json['message_type']
        
        
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.set_name,
            {
                'type':'payload',
                'message_type': type_send,
                'data': data,
            }
        )
        

    def payload(self, event):
        # if self.user.is_authenticated:
        #     print(self.user)
        #sending to every except sender
        if self.channel_name != event.get('sender_channel_name'):

            #send every thing
        # print(event)
        # self.send(text_data=json.dumps(event))

            # print(event)
            self.send(json.dumps({'data':event.get("data"),'message_type':event.get("message_type")}))

