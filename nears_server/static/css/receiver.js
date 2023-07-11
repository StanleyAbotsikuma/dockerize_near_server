var localVideo = document.querySelector('#localVideo'); 
var remoteVideo = document.querySelector('#remoteVideo'); 

var yourConn; 
var stream;
         
       //********************** 
       //Starting a peer connection 
       //********************** 
         
       //getting local video stream 
       navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(function (myStream) { 
          stream = myStream; 
             
          //displaying local video stream on the page 
          localVideo.srcObject = stream;
             
          //using Google public stun server 
          var configuration = { 
             "iceServers": [{ "urls": "stun:stun2.1.google.com:19302" }]
          }; 
             
          yourConn = new RTCPeerConnection(configuration); 
             
          // setup stream listening 
          yourConn.addStream(stream); 
             
          //when a remote user adds stream to the peer connection, we display it 
          yourConn.ontrack = function (e) { 
             remoteVideo.srcObject = e.stream; 
          };
             
          // Setup ice handling 
          yourConn.onicecandidate = function (event) { 
             if (event.candidate) { 
                send({ 
                   type: "candidate", 
                   candidate: event.candidate 
                }); 
             } 
          };  
             
       }).catch(function (error) { 
          console.log(error); 
       }); 
   


//offer handling
       function handleOffer(offer, name) { 
        connectedUser = name; 
        yourConn.setRemoteDescription(new RTCSessionDescription({type: 'offer', sdp: offer.sdp}));
         
        //create an answer to an offer 
        yourConn.createAnswer().then(function (answer) { 
           yourConn.setLocalDescription(new RTCSessionDescription({type: 'answer', sdp: answer.sdp})); 
           send({ 
              type: "answer", 
              answer: answer 
           }); 
        }).catch(function (error) { 
           alert("Error when creating an answer"); 
        }); 
     };