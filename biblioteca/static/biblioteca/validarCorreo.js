$(document).ready(function() {
    // Asume que el campo de correo electrónico tiene el atributo name 'email'
    $('input[name="email"]').on('input', function() {
        // Cuando el contenido del campo de correo electrónico cambie, borra el mensaje de error
        if ($(this).val() === '') {
            $('#newPasswordError').text('');
            $('#newPasswordError').parent().hide();
        }
    });

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
                    localStorage.setItem('showModal', 'true');
                    window.location.href = data.redirect;
                } else {
                    $('#newPasswordError').text('');
                    showModal();
                    $('form').unbind('submit').submit();
                }
            },
            error: function(jqXHR) {
                if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
                    if (jqXHR.responseJSON.error.includes('correu electrònic')) {
                        $('#newPasswordError').text(jqXHR.responseJSON.error);
                        $('#newPasswordError').parent().show();
                    } else {
                        $('#newPasswordError').parent().hide();
                    }
                }
            }
        });
    });
});