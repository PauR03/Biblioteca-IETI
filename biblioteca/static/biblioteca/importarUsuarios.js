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
        var modal = document.getElementById('ModalInfoError');
        var modalContent = modal.querySelector('.modal-content');
        var closeButton = modal.querySelector('.close');

        // Limpiar el contenido del modal antes de agregar nuevos mensajes de error
        modalContent.innerHTML = '';

        if (data.errors) {
            data.errors.forEach(error => {
                var errorParagraph = document.createElement('p');
                // Agrega las etiquetas <br> aquí
                errorParagraph.innerHTML = error + '<br>';
                modalContent.appendChild(errorParagraph);
            });

            modal.style.display = 'block';
        
            closeButton.onclick = function() {
                modal.style.display = 'none';
            }
        
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            }
        } else {
            console.log('Archivo subido con éxito');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});