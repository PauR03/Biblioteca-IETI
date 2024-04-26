$(document).ready(function() {
    // Formulario de envío
    $('form').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token in the request header
            },
            success: function (data) {
                if (data.redirect) {
                    // data.redirect contains the string URL to redirect
                    localStorage.setItem("popup", JSON.stringify([{ status: "success", text: "Benvingut!", timeout: 3000 }]));
                    window.location.href = data.redirect;
                }
            },
            error: function (xhr, errmsg, err) {
                if (xhr.status == 401) {
                    $('#error-message').css({
                        'color': 'red',
                        'font-size': '17px',
                        'font-family': 'Arial'
                    }).text('El correu o la contrasenya son incorrectes');
                }
            }
        });
    });

    // Autocompletado y búsqueda
    var input = $("#search-input");
    var checkbox = $("#available-only");
    var submitButton = $("#search-button");
    var awesomplete = new Awesomplete(input[0]);

    input.on("keyup", function() {
        var query = this.value;
        if (query.length < 3) {
            awesomplete.list = [];
            return;
        }

        $.ajax({
            url: $(this).data('autocomplete-url'),
            data: {
                'q': query,
                'available_only': checkbox.prop('checked')
            },
            dataType: 'json',
            success: function(data) {
                awesomplete.list = data;
            }
        });
    });

    // BUSQUEDA DEL LIBRO (REDIRECCIONAA LA PAGINA)
    submitButton.on('click', function(e) {
        e.preventDefault();
        var query = input.val();
        var url = $(this).data('url');
        window.location.href = url + "?q=" + encodeURIComponent(query);
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