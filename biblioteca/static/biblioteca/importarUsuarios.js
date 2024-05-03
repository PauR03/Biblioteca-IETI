document.getElementById('upload-button').addEventListener('click', function(event) {
    event.preventDefault();

    var form = document.getElementById('upload-form');
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            data.errors.forEach(error => {
                console.log(error);
            });
        } else {
            console.log('Archivo subido con éxito');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});