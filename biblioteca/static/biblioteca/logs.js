function saveLog(tipus, informacio, ruta, usuari) {
    if (usuari === null) {
        usuari = 'unknown';
        console.error('No se pudo obtener el nombre de usuario del localStorage');
    }

    let logs;
    try {
        logs = JSON.parse(localStorage.getItem('logs')) || [];
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

    logs.push(newLog);

    localStorage.setItem('logs', JSON.stringify(logs));

    if (logs.length >= 10) {
        sendLogs(logs);
        logs = [];
        localStorage.setItem('logs', JSON.stringify(logs));
    }
}

function sendLogs(logs) {
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
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}