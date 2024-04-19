$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            success: function(data) {
                if (data.redirect) {
                    // data.redirect contains the string URL to redirect
                    window.location.href = data.redirect;
                }
            },
            error: function(xhr, errmsg, err) {
                if (xhr.status == 401) {
                    $('#error-message').css({
                        'color': 'red',
                        'font-size': '18px',
                        'font-family': 'Arial'
                    }).text('El correu o la contrasenya son incorrectes');
                }
            }
        });
    });
});