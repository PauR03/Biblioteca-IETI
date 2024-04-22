function createLogs(logs) {
    const url = '/api/create_log/';  // Asegúrate de reemplazar esto con la URL correcta de tu API

    logs.forEach(log => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Asegúrate de incluir el token CSRF si estás usando la protección CSRF de Django
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(log)
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
    });
}