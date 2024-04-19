// JavaScript
// Get the modals
var errorModal = document.getElementById("myModal");
var successModal = document.getElementById("mySuccessModal");

// Get the <span> elements that close the modals
var errorSpan = document.getElementsByClassName("close")[0];
var successSpan = document.getElementsByClassName("success-close")[0];

// When the page loads, open the modal if there are any messages
window.onload = function() {
  var messages = document.querySelectorAll('.modal .modal-content p');
  messages.forEach(function(message) {
    if (message.parentElement.parentElement.id === 'mySuccessModal') {
      // Show success popup
      successModal.style.display = "block";
    } else if (message.parentElement.parentElement.id === 'myModal') {
      // Show error popup
      errorModal.style.display = "block";
    }
  });
}

// When the user clicks on <span> (x), remove the modal
errorSpan.onclick = function() {
  errorModal.remove();
}

successSpan.onclick = function() {
  successModal.remove();
}