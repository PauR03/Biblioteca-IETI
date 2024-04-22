function saveLog(tipus, informacio, ruta, usuari) {
    console.log('saveLog called with:', { tipus, informacio, ruta, usuari });

    if (usuari === null) {
        usuari = 'unknown';
        console.error('No se pudo obtener el nombre de usuario del localStorage');
    }

    let logs;
    try {
        logs = JSON.parse(localStorage.getItem('logs')) || [];
        console.log('Parsed logs:', logs);
    } catch (e) {
        console.error('Error al parsear los logs del localStorage:', e);
        logs = [];
    }

    let newLog = {
        tipus: tipus,
        informacio: informacio,
        ruta: ruta,
        usuari: usuari
    };
    console.log('New log:', newLog);

    logs.push(newLog);
    console.log('Logs after push:', logs);

    localStorage.setItem('logs', JSON.stringify(logs));
    console.log('Logs saved to localStorage');

    if (logs.length >= 10) {
        console.log('Sending logs to API');
        sendLogs(logs);
        logs = [];
        localStorage.setItem('logs', JSON.stringify(logs));
        console.log('Logs cleared');
    }
}

function sendLogs(logs) {
    console.log('sendLogs called with:', logs);
    const url = '/api/create_log/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },  
        body: JSON.stringify(logs)
    })
    .then(response => {
        console.log('Response received:', response);
        if (!response.ok) {
            console.error('Server response was not ok:', response.status, response.statusText);
        }
        if (response.headers.get('Content-Type') !== 'application/json') {
            console.error('Server response was not JSON:', response.headers.get('Content-Type'));
            // Read the response as text instead of JSON
            return response.text();
        }
        return response.json();
    })
    .then(data => {
        if (typeof data === 'string') {
            // Handle non-JSON response
            console.error('Non-JSON response:', data);
        } else {
            console.log('Data received:', data);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}