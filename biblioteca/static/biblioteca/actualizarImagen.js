$(window).on('load', function() {
    $.get('/get_profile_image/', function(data) {
        var profileImage = data.imatgePerfil;
        console.log(profileImage);
        if(profileImage) {
            $("#profile-image").attr("src", profileImage);
        } else {
            console.log("Profile image URL is not set. Setting default profile image.");
            var defaultImage = $("#profile-image").attr("data-default");
            $("#profile-image").attr("src", defaultImage);
        }
    });
});