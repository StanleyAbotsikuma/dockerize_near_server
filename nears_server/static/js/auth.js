
let URL = window.location.host;
let Protocol = 'http://';
let ProtocolWs = 'ws://' ;

let responses;


function saveSessionData(data) {
    // const key = CryptoJS.lib.WordArray.random(16);
    // const encryptedData = CryptoJS.AES.encrypt(data, key.toString());
    localStorage.setItem('session_data', data);
    // localStorage.setItem('session_key', key.toString());
}

function sign_in() {
    var getPhone_number = document.getElementById("phone_number").value;
    var getPassword = document.getElementById("password").value;
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: getPhone_number, password: getPassword })
    };
    fetch(Protocol + URL + '/api/login/', requestOptions)
        .then(async response => {
            if (!response.ok) {
                throw new Error(`Error! status: ${response.status}`);
            }
            const result = await response.json();
            localStorage.setItem('access_token', result.access);
            localStorage.setItem('refresh_token', result.refresh);
            // saveSessionData(result.access);
            window.location.href = 'http://' + URL + '/useragent/';
        })
        .catch(error => {
            console.error(error);
        });
}


function launchPage() {
    const accessToken = localStorage.getItem('access_token');
    const requestOptions = {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${accessToken}` }
    };

    fetch('/api/data/', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to retrieve data');
            }
            return response.json();
        })
        .then(data => {
            // Handle the response data
        })
        .catch(error => {
            console.error(error);
        });


}

function signupFunction() {
    let usergent = (navigator.userAgent).toString().slice(0, 90);
    let getEmail = document.getElementById("email").value;
    let getPhone_number = document.getElementById("phone_number").value;
    let getDevice_id = document.getElementById("device_id").value;
    let getPassword = document.getElementById("confirm_password").value;
    let data = {
        email: getEmail,
        phone_number: getPhone_number,
        device_id: usergent,
        password: getPassword
    }
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    };
    fetch(Protocol + URL + '/api/create_account/', requestOptions)
        .then(response => {
            if (response.ok) {
                sign_in_sign_up(getPhone_number, getPassword);
            }
        })
        .catch(error => {
            console.error(error);
        });
}
function staffSignupFunction() {
    let getStaff_username = document.getElementById("staff_username").value;
    let getFirstName = document.getElementById("first_name").value;
    let getLastname = document.getElementById("last_name").value;
    let getPosition = document.getElementById("position").value;
    const accessToken = localStorage.getItem('access_token');

    let data = {
        staff_username: getStaff_username,
        first_name: getFirstName,
        last_name: getLastname,
        position: getPosition
    }


    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${accessToken}` },
        body: JSON.stringify(data)
    };
    fetch(Protocol + URL + '/api/staff/', requestOptions)
        .then(response => {
            if (response.ok) {
                window.location.href = 'http://' + URL + '/useragent/';
            }

        })
        .catch(error => {
            console.error(error);
        });

}


function refreshFunction() {


    // Retrieve the refresh token from local storage or a cookie
    const refreshToken = localStorage.getItem('refresh_token');

    // Set up the request options
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken })
    };

    // Make the request to the server to obtain a new access token
    fetch('/api/token/refresh/', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to refresh token');
            }
            return response.json();
        })
        .then(data => {
            // Store the new access token in local storage or a cookie
            localStorage.setItem('access_token', data.access);
        })
        .catch(error => {
            console.error(error);
        });
}
function sign_in_sign_up(getPhone_number, getPassword) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: getPhone_number, password: getPassword })
    };
    fetch(Protocol + URL + '/api/login/', requestOptions)
        .then(async response => {
            if (!response.ok) {
                throw new Error(`Error! status: ${response.status}`);
            }
            const result = await response.json();
            localStorage.setItem('access_token', result.access);
            localStorage.setItem('refresh_token', result.refresh);
            saveSessionData(result.access);
            toggleForm();


        })
        .catch(error => {
            console.error(error);
        });
}