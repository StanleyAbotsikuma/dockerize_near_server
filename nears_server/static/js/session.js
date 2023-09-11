
let URL = window.location.host;
let Protocol = 'http://' ;
let ProtocolWs = 'ws://' ;


function isAuthenticated() {
    const sessionData =  localStorage.getItem('access_token');
  
    if (sessionData) {
    
      return true;
    } else {
      
      return false;
    }
  }
if (isAuthenticated()) {
   
} else {
    window.location.href = Protocol+ URL +'/useragent/signin';
}
