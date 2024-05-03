$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.redirect) {
                    // Si el servidor devuelve una URL de redirección, redirige a esa URL
                    // Pero primero, almacena una variable en localStorage para indicar que se debe mostrar el modal
                    localStorage.setItem('showModal', 'true');
                    window.location.href = data.redirect;
                } else {
                    // Si no hay error, limpia los mensajes de error
                    $('#newPasswordError').text('');
                    // Muestra el modal
                    showModal();
                    // Envía el formulario normalmente
                    $('form').unbind('submit').submit();
                }
            },
            error: function(jqXHR) {
                // Si la respuesta contiene un error, muéstralo en el elemento correspondiente
                if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
                    if (jqXHR.responseJSON.error.includes('correu electrònic')) {
                        $('#newPasswordError').text(jqXHR.responseJSON.error);
                    }
                }
            }
        });
    });
});