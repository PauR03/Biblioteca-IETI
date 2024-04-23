$('form').on('submit', function (e) {
    var newPassword = $('input[name="new_password"]').val();
    var confirmNewPassword = $('input[name="confirm_new_password"]').val();
    const inputDate = $('#dataNaixament').val()

    if (newPassword !== confirmNewPassword) {
        e.preventDefault();
        createPopup({ status: "error", text: "Les contrasenyes no coincideixen" });

    } else {
        localStorage.setItem("popup", JSON.stringify([{ status: "success", text: "Canvis realitzats correctament", timeout: 3000 }]));
    }

    if (inputDate > new Date().toISOString().split('T')[0]) {
        e.preventDefault();
        createPopup({ status: "error", text: "La data de naixament no pot ser futura" });
    }
});