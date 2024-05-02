document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // Necessario para Django procesar la solicitud como AJAX
            'X-CSRFToken': this.querySelector('input[name="csrfmiddlewaretoken"]').value, // Obtén el token CSRF del formulario
        },
    })
    .then(response => {
        if (!response.ok) throw new Error(response.statusText);
        return response.json();
    })
    .then(data => {
        if (data.error) {
            document.getElementById('email-error').textContent = data.error; // Muestra el mensaje de error
        } else {
            alert('Usuario creado con éxito');
            location.reload();
        }
    })
    .catch(error => alert(error));
});