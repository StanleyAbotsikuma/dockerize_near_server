from django.core.cache import cache

class AgentClass:
    def __init__(self, agent_id,index):
        self._agent_id=agent_id
        self._lessbusy  = True
        self._index =index
    def __str__(self):
        return str(self._lessbusy)
    def getIndex(self):
        return self._index
    def getState(self):
        return self._lessbusy
    def getAgent(self):
        return self._agent_id
    def setState(self,lessbusy):
        self._lessbusy =lessbusy
    
class CaseClass:
    def __init__(self,case_id,user_id,index):
        self._case_id=case_id
        self._user_id =user_id
        self._index=index
    def getCaseID(self):
        return self._case_id
    def getUserID(self):
        return self._user_id
    def getIndex(self):
        return self._index
    
    
case_key = "case_cache_list"
agent_key = "agent_cache_list"

def case_function(action,case_instance):
    if action=="add":
        try:      
            g = list(cache.get(case_key))
            g.append(case_instance)
            cache.set(case_key,g) 
            for i in cache.get(case_key):
                print(f'the id = {i.getCaseID()} the index = {i.getIndex()}')
            
        except:
            l = []
            l.append(case_instance)
            cache.set(case_key,l) 
    elif action=="remove":
        try:
            g = list(cache.get(case_key))
            n = []
            # del g[case_instance]
            for i in g:
                if i.getCaseID() != case_instance:
                    n.append(i)
                    # print("not me")
                else:
                    print(i.getCaseID() + " No  Remove")
            
            cache.set(case_key,n) 
        except:
            pass            
        
def agent(action,agent_instance):
    if action =="add":
        try:
            g = list(cache.get(agent_key))
            g.append(agent_instance)
            cache.set(agent_key,g) 
            for i in cache.get(agent_key):
                print(f'the id = {i.getAgent()} the index = {i.getIndex()}')
        except:
            l = []
            l.append(agent_instance)
            cache.set(agent_key,l) 
            
    elif action == "remove":
        try:
            g = list(cache.get(agent_key))
            # issue////////////////////////////////////////////////////////////////////////////////////////////////////
             # issue////////////////////////////////////////////////////////////////////////////////////////////////////
            n =[]
             # issue////////////////////////////////////////////////////////////////////////////////////////////////////
             # issue////////////////////////////////////////////////////////////////////////////////////////////////////

            for i in g:
                if i.getAgent() != agent_instance:
                    n.append(i)
                else:
                    print(i.getAgent() + " Removed")
            cache.set(agent_key,n) 
            # print (f'successfully remove {agent_instance}')
        except:
            pass
def check_live_agents():
    if cache.has_key(agent_key):
        g = list(cache.get(agent_key))
        for i in g:
            if i.getState() == True:
                return i.getAgent()
            else:
                return None
    else:
        return None
    
    
def check_exit_agents(agent_id):
    if cache.has_key(agent_key):
        g = list(cache.get(agent_key))
        for i in g:
            # print(i.getAgent())
            if i.getAgent() == agent_id:
                return True
            else:
                return None
    else:
        return None
      
        
def update_agent(action,agent_index):
    if action == "busy":
        try:
            g = list(cache.get(agent_key))
            n =[]
            for i in g:
                if  i.getAgent() == agent_index:
                    i.setState(False)
                    print(i.getAgent() + " No  Busy")
                n.append(i)
            cache.set(agent_key,n)
        except:
            pass
                 
    elif action =="lessbusy":
        g = list(cache.get(agent_key))
        n =[]
        for i in g:
            if  i.getAgent() == agent_index:
                i.setState(True)
                print(i.getAgent() + " Yes less Busy")
            n.append(i)
        cache.set(agent_key,n)
        try:
            if len(cache.get(case_key)) > 0:
                g = list(cache.get(case_key))
                oldCaseID = g[0].getCaseID()
                del g[0]
                cache.set(case_key,g)
                assignWhenLessBusy(oldCaseID,agent_index)
        except:
            pass
            
            
            
            
def assignWhenLessBusy(caseid,agentName):
    from rest_server.models import Case,Status,Staff
    case = Case.objects.get(pk=caseid)
    status=Status.objects.get(pk="STATUS_ASSIGNED")
    staff=Staff.objects.get(pk=agentName)
    case.status=status
    case.received_by=staff
    case.save()