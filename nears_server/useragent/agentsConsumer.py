import json

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
        
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_type = text_data_json['message_type']
        recipient_username = text_data_json['recipient_username']

        # send chat message event to the recipient user
        recipient_channel_name = self.get_recipient_channel_name(recipient_username)
        if recipient_channel_name:
            self.send(json.dumps({
                'type': 'websocket.send',
                'message': message,
                'message_type': message_type,
                'sender_username': str(self.user),
                'recipient_username': recipient_username,
            }))

    def get_recipient_channel_name(self, recipient_username):
    
        for channel_name in self.channel_layer.group_channels(self.set_name):
            consumer = self.channel_layer.registry.get_consumer(channel_name)
            if consumer.user.username == recipient_username:
                return channel_name
        return None