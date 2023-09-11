let URL = window.location.host;
let Protocol = 'http://' ;
let ProtocolWs = 'ws://' ;




function staffLoadFunction() {
    const accessToken = localStorage.getItem('access_token');


    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' , 'Authorization': `Bearer ${accessToken}`},
      body: JSON.stringify(data)
    };
    fetch(Protocol + URL + '/api/staff/', requestOptions)
        .then(async response => {
            if (response.ok) {
                const result = await response.json();
                console.log(result);

            }

        })
        .catch(error => {
            console.error(error);
        });

}

