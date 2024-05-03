$(document).ready(function() {
    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Show the modal
    window.showModal = function() {
        modal.style.display = "block";

        // Set a timer to hide the modal after 3 seconds
        setTimeout(function() {
            modal.style.display = "none";
        }, 900000); // 3000 milliseconds = 3 seconds
    }

    // If the 'showModal' variable is in localStorage, show the modal and remove the variable
    if (localStorage.getItem('showModal')) {
        showModal();
        localStorage.removeItem('showModal');
    }
});