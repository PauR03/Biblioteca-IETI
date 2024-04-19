$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token in the request header
            },
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

// Function to get a cookie by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}