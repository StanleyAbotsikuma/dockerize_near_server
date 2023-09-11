import json
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_server.models import Case, User,UserAuth,Mode,Status,Staff
from useragent.assignALGO import *
class emergencyConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.set_name = None
        self.name = None
        self.user = None
       
    def connect(self):
        self.user = self.scope['user']
        self.set_name = f'caller_{self.user}'
        self.caseIndex= ""
        self.current_agent = ""
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
        
        if self.current_agent != "":
            async_to_sync(self.channel_layer.group_send)(
                f'agent_{self.current_agent}',
                {
                    'type':'payload',
                    'message_type': "caller_ended",
                    'data': [],
                    'receiver': "agent",
                    
                }
            )   
              
        else:
            case_function("remove",self.caseIndex)
              
       

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # print(text_data_json)
        receiver = text_data_json['receiver']
        if receiver == "nears":
            user=User.objects.get(phone_number=self.user)
            place=text_data_json['data'][1]
            location=text_data_json['data'][0]
            mode=Mode.objects.get(pk="MODE_31071256")
            status=Status.objects.get(pk="STATUS_PENDING")
            case = Case.objects.create(user_id=user,mode_id=mode,status=status,place=place,location=location)
            case.save()
            aGent = check_live_agents()
            if aGent == None:
                self.caseIndex=noAgent(self.set_name,case)
            else:
                status=Status.objects.get(pk="STATUS_ASSIGNED")
                staff=Staff.objects.get(pk=aGent)
                case.status=status
                case.received_by=staff
                case.save()
                
        
            
        elif receiver == "agent":
            type = text_data_json['type']
            data =text_data_json['data']
                
            async_to_sync(self.channel_layer.group_send)(
                    f'agent_{text_data_json["to"]}',
                    {
                        'type':'payload',
                        'message_type': type,
                        'data': data,
                        'receiver': receiver,
                        
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
        if event.get('from') != None or event.get('from') !="":
            self.current_agent = event.get('from')
        if self.channel_name != event.get('sender_channel_name'):
            self.send(json.dumps({'data':event.get("data"),'type':event.get("message_type"),'receiver':event.get("receiver"),'from':event.get("from")}))


def noAgent(caller_name,case):
    set_index = 0
    try:
        set_index = len(cache.get(case_key))
    except:
        pass
    case_function("add",CaseClass(case.pk,caller_name,set_index))
    return case.pk