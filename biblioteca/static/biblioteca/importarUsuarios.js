document.getElementById('upload-button').addEventListener('click', function(event) {
    event.preventDefault();

    var form = document.getElementById('upload-form');
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log(response);
        return response.json();
    })
    .then(data => {
        if (data.errors) {
            var modal = document.getElementById('ModalInfoError');
            var modalContent = modal.querySelector('.modal-content');
            var closeButton = modal.querySelector('.close');

            modalContent.innerHTML = '';

            console.log(data.errors);
        
            var closeButton = document.createElement('span');
            closeButton.className = 'close';
            closeButton.innerHTML = '&times;';
        
            modalContent.appendChild(closeButton);
        
            data.errors.forEach(error => {
                var errorParagraph = document.createElement('p');
                var errorNode = document.createTextNode(error);
                errorParagraph.appendChild(errorNode);
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
            console.log(data.success);
            window.showModal();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});