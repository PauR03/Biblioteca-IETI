document.querySelector('form').addEventListener('submit', function(e) {
    var newPassword = document.querySelector('input[name="new_password"]').value;
    var confirmNewPassword = document.querySelector('input[name="confirm_new_password"]').value;

    if (newPassword !== confirmNewPassword) {
        e.preventDefault();
        document.getElementById('error-message').textContent = 'Les contrasenyes no coincideixen';
        $('#error-message').css({
            'color': 'red',
            'font-size': '15px',
            'font-family': 'Arial',
            'margin-left': '410px'
        });
    } else {
        document.getElementById('error-message').textContent = '';
        // No need to prevent form submission if passwords match
    }
});