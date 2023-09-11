import json
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_server.models import Case, User,UserAuth,Mode,Status,Staff
from useragent.assignALGO import *
class agentsConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.set_name = None
        self.name = None
        self.user = None
        self.agent_index =None
    def connect(self):
        self.user = self.scope['user']
        self.set_name = f'agent_{self.user}'
        # print(self.set_name)
        self.accept()


        async_to_sync(self.channel_layer.group_add)(
            self.set_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.set_name,
            self.channel_name,
        )
        try:
            if self.agent_index != None:
                agent("remove",self.agent_index)
            
        except:
            pass
        
        

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # print(text_data_json)
        receiver = text_data_json['receiver']
        if receiver == "nears":
            type = text_data_json['type']
            data =text_data_json['data']
            if type == "addAgent":
                return_index =addAgent(data[0])
                if return_index !=None:
                    self.agent_index=return_index
                    async_to_sync(self.channel_layer.group_send)(
                self.set_name,
                {
                    'type':'minimalPayload',
                    'message_type': "index_returns",
                    'data': [return_index],
                    'receiver': "agent",
                })                    
            
            elif type == "agentBusy":
                update_agent("busy",data[0])
            elif type == "agentLessBusy":
                update_agent("lessbusy",data[0])
        
        elif receiver == "caller":
            type = text_data_json['type']
            data =text_data_json['data']
            async_to_sync(self.channel_layer.group_send)(
                f"caller_{text_data_json['to']}",
                {
                    'type':'payload',
                    'message_type': type,
                    'data': data,
                    'receiver': receiver,
                    'from':self.user.phone_number
                    
                }
            )   
            
        

        else:
            type = text_data_json['type']
            data =text_data_json['data']
        
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
        print(event)
        if self.channel_name != event.get('sender_channel_name'):
            self.send(json.dumps({'data':event.get("data"),'type':event.get("message_type"),'receiver':event.get("receiver")}))
    
    
    def minimalPayload(self, event):
        if self.channel_name != event.get('sender_channel_name'):
            self.send(json.dumps({'data':event.get("data"),'type':event.get("message_type"),'receiver':event.get("receiver")}))

    


def addAgent(agent_name):
    set_index = 0
    try:
        set_index = len(cache.get(agent_key))
    except:
        pass
    
    if check_exit_agents(agent_name)== None:
        agent("add",AgentClass(agent_name,set_index))
        return agent_name
    else:

        print("already exist")
        return None
    