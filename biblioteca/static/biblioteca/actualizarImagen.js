$(window).on('load', function () {
    $.get('/get_profile_image/', function (data) {
        var profileImage = data.imatgePerfil;
        if (profileImage) {
            $("#profile-image").attr("src", profileImage);
        } else {
            var defaultImage = $("#profile-image").attr("data-default");
            $("#profile-image").attr("src", defaultImage);
        }
    });
});