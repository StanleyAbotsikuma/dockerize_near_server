// Agent local variables 
const accessToken = localStorage.getItem('access_token');
const onlineStatus = document.querySelector('.online-status');
//addition

const fullName = '';
let staffId = '';
let staffIndex = 0;
let agentSocket;
let gData;

// Case Local variables
// 
// 
let CaseID = "";
let UserID = "";
let processState = 0;
var latitude = 0;
var longitude = 0;
// 
//
//web rtc
var webrtcConnection;
var stream;
var remoteVideo=document.querySelector("#remoteVideo");

//
//////
///////////////

const form_caseId = document.querySelector('#case_id');
const form_type = document.querySelector('#type');
const form_mode = document.querySelector('#mode');
const form_caseName = document.querySelector('#case');
const form_userId = document.querySelector('#user_id');
const form_status = document.querySelector('#status');
const form_resourceId = document.querySelector('#resource_id');
const form_location = document.querySelector('#location');
const form_place = document.querySelector('#place');
const form_realtimeUpdates = document.querySelector('#realtime_updates');
const form_receivedBy = document.querySelector('#received_by');
// 
// 
function setOnlineStatus() {
  onlineStatus.textContent = 'Online';
  onlineStatus.style.color = 'green';
}

function setOfflineStatus() {
  onlineStatus.textContent = 'Offline';
  onlineStatus.style.color = '#f44336';
}
//
//////
///////////////
//web socket init
agentSocket = new ReconnectingWebSocket(ProtocolWs + URL + "/ws/agents/?token=" + accessToken, null, { debug: true, reconnectInterval: 3000 });
agentSocket.onclose = function (e) {
  window.location.href = Protocol + URL + '/useragent/signin';
}
//
//////
///////////////
//on load function
window.onload = function () {
  staffLoadFunction();
  initiate();

  // additions
  opions();
}

function toggleButton() {
  var button = document.querySelector(".toggle-button");
  if (button.classList.contains("online")) {
    agentBusy();
    agentSocket.send(JSON.stringify({
      "receiver": "nears",
      "type": "agentBusy",
      "data": [staffIndex]
    }));
  } else {
    agentLessBusy();
    agentSocket.send(JSON.stringify({
      "receiver": "nears",
      "type": "agentLessBusy",
      "data": [staffIndex]
    }));
  }
}

//
//////
///////////////
//load staff
function staffLoadFunction() {
  const requestOptions = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${accessToken}` }
  };
  fetch(Protocol + URL + '/api/staff/', requestOptions)
    .then(async response => {
      if (response.ok) {
        const result = await response.json();

        document.querySelector('.full-name').textContent = result.first_name + " " + result.last_name;
        document.querySelector('.staff-id').textContent = result.staff_id;

        agentSocket.send(JSON.stringify({
          "receiver": "nears",
          "type": "addAgent",
          "data": [result.staff_id]
        }));
      }

    })
    .catch(error => {
      console.error(error);
    });

}
function getType(data) {
  if (data.receiver == "agent") {
    switch (data.type) {
      // set index
      case "index_returns":
        staffIndex = data.data[0];
        console.log("agent Login done");
        break;
      // set status
      case "change_status":
        gData = data.data[0];
        if (gData == "agentBusy") {
          agentBusy();
        }
        else if (gData == "agentLessBusy") {
          agentLessBusy();
        };
        break;
      case "cases":
        loadCase(data.data);
        break;

      case "answer":
        // console.log(data.data);
        handleAnswer(data.data[0], data.data[1]);
        break;
      case "candidate":
        handleCandidate(data.data[0]);
        break;

      case "caller_ended":
        toggleButton();
        break;
      default:
        break;
    }
  }
};

agentSocket.onmessage = function (e) {
  var data = JSON.parse(e.data);
  getType(data);
}

function agentBusy() {
  var button = document.querySelector(".toggle-button");

  button.classList.remove("online");
  button.classList.add("offline");
  button.querySelector("span").textContent = "Offline";
}
function agentLessBusy() {
  var button = document.querySelector(".toggle-button");
  button.classList.remove("offline");
  button.classList.add("online");
  button.querySelector("span").textContent = "Online";
  closeCase();

  try {
    remoteVideo.srcObject = null;
  webrtcConnection.onicecandidate = null;
  webrtcConnection.ontrack = null;
  } catch (error) {
    
  }
  

}

function loadCase(data) {
  processState = 1;
  
  latitude =String(data[7]).split(",")[1];
  longitude =String(data[7]).split(",")[0];
  CaseID = data[0];
  UserID = data[11];

  form_caseId.value = data[0];
  form_type.value = data[1];
  form_mode.value = data[2];
  form_caseName.value = data[3];
  form_userId.value = data[4];
  form_status.value = data[5];
  form_resourceId.value = data[6];
  form_location.value = data[7];
  form_place.value = data[8];
  form_realtimeUpdates.checked = data[9];
  form_receivedBy.value = data[10];
  agentBusy();
  createOffer()
}
function closeCase() {


  form_caseId.value = "";
  form_type.value = "";
  form_mode.value = "";
  form_caseName.value = "";
  form_userId.value = "";
  form_status.value = "";
  form_resourceId.value = "";
  form_location.value = "";
  form_place.value = "";
  form_realtimeUpdates.checked = false;
  form_receivedBy.value = "";
  CaseID = "";
  UserID = "";
  processState = 0;
}






function initiate() {

  navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(function (myStream) {

    var configuration = {
      "iceServers": [
        { "urls": "stun:stun1.l.google.com:19302" },
        { "urls": "stun:stun2.l.google.com:19302" }]
    };

    webrtcConnection = new RTCPeerConnection(configuration);
    webrtcConnection.addStream(myStream);
    // localRecorder = new MediaRecorder(stream);
    // localRecorder.ondataavailable = handleLocalDataAvailable;
    // localRecorder.start();

// addition
    webrtcConnection.addEventListener('track', async (event) => {
      const [remoteStream] = event.streams;
      remoteVideo.srcObject = remoteStream;
      // console.log(remoteStream +" seconds");
    //   remoteRecorder = new MediaRecorder(remoteStream);
    //   remoteRecorder.ondataavailable = handleRemoteDataAvailable;
    //  remoteRecorder.start()

  });
    webrtcConnection.onicecandidate = function (event) {

      if (event.candidate) {
        send({

          "receiver": "caller",
          "type": "candidate",
          "data": [event.candidate.candidate, event.candidate.sdpMid, event.candidate.sdpMLineIndex],
          "to": UserID
        }
        );
      }

    };
  }).catch(function (error) {
    console.log(error);
  });

};



function createOffer() {
  webrtcConnection.createOffer().then(function (offer) {
    webrtcConnection.setLocalDescription(offer);
    send({

      "receiver": "caller",
      "type": "offer",
      "data": [offer.type, offer.sdp],
      "to": UserID
    });
  }).catch(function (error) {
    alert("Error when creating an offer");
  });
}


function handleAnswer(type, sdp) {
  webrtcConnection.setRemoteDescription(new RTCSessionDescription({ sdp, type }));
};

function handleCandidate(candidate) {
  webrtcConnection.addIceCandidate(candidate).then(() => {
    console.log("Ice candidate successfully added")
  })
    .catch(error => {
      console.log(" Failed to add ice candidate");
    });;

};

function send(message) {
  agentSocket.send(JSON.stringify(message));
};




// addition

function opions(){
// Get the select element
const selectElement = document.getElementById('type');
const option = document.createElement('option');
      option.text = "---";
      option.value = "";
selectElement.add(option);
fetch(Protocol + URL + '/api/case_types/')
  .then(response => response.json())
  .then(data => {
    data.forEach(item => {
      const option = document.createElement('option');
      option.text = item.name;
      option.value = item.value;
   
      selectElement.add(option);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });}

        function viewLocation() {
          if (processState> 0)
          {
            document.getElementById("viewLocation").style.display = "block";
            loadOpenStreetMap();
          }else{
            alert("No Active Case");
          }
        }

        function closeModal() {
            document.getElementById("viewLocation").style.display = "none";
        }
        function loadOpenStreetMap() {
            var map = L.map('map').setView([latitude, longitude], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
            }).addTo(map);
            L.marker([latitude, longitude]).addTo(map);
        }


        function viewDepartments() {
          document.getElementById("viewDepartments").style.display = "block";

          if (processState> 0)
          {
            document.getElementById("viewDepartments").style.display = "block";
            loadOpenStreetMap();
          }else{
            alert("No Active Case");
          }
        }

        function closeModalDepartments() {
          document.getElementById("viewDepartments").style.display = "None";
      }





//       let localStream;
// let remoteStream;
// let localRecorder;
// let remoteRecorder;

// // Get local and remote streams using getUserMedia or any other method
// navigator.mediaDevices.getUserMedia({ audio: true, video: true })
//   .then(stream => {
//     localStream = stream;
//     // Attach local stream to a video element
//     const localVideoElement = document.getElementById('local-video');
//     localVideoElement.srcObject = stream;

//     // Create a MediaRecorder for local stream
//     localRecorder = new MediaRecorder(stream);
//     localRecorder.ondataavailable = handleLocalDataAvailable;
//     localRecorder.start();
//   })
//   .catch(error => {
//     console.error('Error accessing local media devices:', error);
//   });

// // Get remote stream from a peer connection
// const peerConnection = new RTCPeerConnection();

// // Assuming you have set up the peer connection and added remote tracks

// // Listen for remote stream
// peerConnection.addEventListener('track', event => {
//   remoteStream = event.streams[0];
//   // Attach remote stream to a video element
//   const remoteVideoElement = document.getElementById('remote-video');
//   remoteVideoElement.srcObject = remoteStream;

//   // Create a MediaRecorder for remote stream
//   remoteRecorder = new MediaRecorder(remoteStream);
//   remoteRecorder.ondataavailable = handleRemoteDataAvailable;
//   remoteRecorder.start();
// });

// // Handle data available event for local recorder
// function handleLocalDataAvailable(event) {
//   if (event.data.size > 0) {
//     // Store locally recorded data or send it to server for further processing
//     // For example, you can store it in an array or upload to a server
//     const localRecordedData = event.data;
//   }
// }

// // Handle data available event for remote recorder
// function handleRemoteDataAvailable(event) {
//   if (event.data.size > 0) {
//     // Store remotely recorded data or send it to server for further processing
//     // For example, you can store it in an array or upload to a server
//     const remoteRecordedData = event.data;
//     saveRecordedData(remoteRecordedData, 'remote-video-recording.webm');
//   }
// }



// function saveRecordedData(data, filename) {
//   const blob = new Blob([data], { type: 'video/webm' });

//   const a = document.createElement('a');
//   a.href = URL.createObjectURL(blob);
//   a.download = filename;
//   a.style.display = 'none';
//   document.body.appendChild(a);
//   a.click();
//   document.body.removeChild(a);
// }