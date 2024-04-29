$(document).ready(function () {
    const passwordValidation = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,16}$/;

    function validatePassword(input) {
        const $input = $(input);
        const $errorMessage = $('#newPasswordError');

        if ($input.val() === '' || $input.val() === null || $input.val() === undefined) {
            $errorMessage.text('');
            return true;
        } else if (!passwordValidation.test($input.val())) {
            $errorMessage.text('Ha de tenir 8-16 caràcters, majúscules, minúscules, un símbol i un número.');
            saveLog('Error', 'La contraseña no cumple los parametros', window.location.pathname, localStorage.getItem('username'));

            return false;
        } else {
            $errorMessage.text('');
            return true;
        }
    }

    function validatePasswordMatch() {
        const newPassword = $('input[name="new_password"]').val();
        const confirmPassword = $('input[name="confirm_new_password"]').val();
        const $errorMessage = $('#confirmPasswordError');

        if (newPassword === '' || confirmPassword === '') {
            $errorMessage.text('');
            return true;
        } else if (newPassword !== confirmPassword) {
            $errorMessage.text('Les contrasenyes no coincideixen.');
            saveLog('Error', 'Las contraseñas no coinciden', window.location.pathname, localStorage.getItem('username'));

            return false;
        } else {
            $errorMessage.text('');
            return true;
        }
    }

    $('input[name="new_password"]').on('blur', function () {
        validatePassword(this);
    });

    $('input[name="confirm_new_password"]').on('blur', function () {
        validatePasswordMatch();
    });

    $('form').on('submit', function (e) {
        if (!validatePassword($('input[name="new_password"]')) || !validatePasswordMatch()) {
            e.preventDefault();
        }
    });
});