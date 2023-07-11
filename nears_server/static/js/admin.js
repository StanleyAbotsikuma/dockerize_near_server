const onlineStatus = document.querySelector('.online-status');
const fullName = 'Stanley Abotsikuma'; 
const staffId = 'Staff_1234'; 

function setOnlineStatus() {
  onlineStatus.textContent = 'Online';
  onlineStatus.style.color = 'green';
}

function setOfflineStatus() {
  onlineStatus.textContent = 'Offline';
  onlineStatus.style.color = '#f44336';
}


window.onload = function() {
  // setOnlineStatus();
  document.querySelector('.full-name').textContent = fullName;
  document.querySelector('.staff-id').textContent = `Staff ID: ${staffId}`;
} 


function toggleButton() {
  var button = document.querySelector(".toggle-button");
  if (button.classList.contains("online")) {
    button.classList.remove("online");
    button.classList.add("offline");
    button.querySelector("span").textContent = "Offline";
  } else {
    button.classList.remove("offline");
    button.classList.add("online");
    button.querySelector("span").textContent = "Online";
  }
}
