
let URL = window.location.host;
let Protocol = 'http://' ;
function getSessionData() {
  // Get the encrypted session data from the local storage variable
  const encryptedData = localStorage.getItem('session_data');

  // Get the encryption key from the local storage variable
  const key = localStorage.getItem('session_key');

  // Check if the session data and encryption key are present
  if (encryptedData && key) {
    // Decrypt the session data using AES
    const decryptedData = CryptoJS.AES.decrypt(encryptedData, key).toString(CryptoJS.enc.Utf8);

    // Parse the decrypted JSON data and return it
    return JSON.parse(decryptedData);
  } else {
    // Session data not found, return null
    return null;
  }
}
function isAuthenticated() {
    const sessionData = getSessionData();
  
    if (sessionData && sessionData.user_id) {
    
      return true;
    } else {
      
      return false;
    }
  }
if (isAuthenticated()) {
   
} else {
    window.location.href = Protocol+ URL +'/useragent/signin';
}
