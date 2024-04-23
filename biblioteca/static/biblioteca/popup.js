// createPopup({ status: "error", text: "Usuari o contrasenya incorrectes Usuari o contrasenya incorrectes Usuari o contrasenya incorrectes", timeout: 5000 });
// createPopup({ status: "success", text: "Usuari o contrasenya correctes jaksjfkl eof esajfdsaklfjlksdajfkladsjfkldsjkfl es fsa asdjkfjadsklfj as k" });
/**
 * Hola no se que hago
 * @param status {String} - Status of the popup (success, error)
 * @param text {String} - Text of the popup
 * @param timeout {Number} - Time in milliseconds to hide the popup
 * @returns Nothing 
 */
function createPopup({ status, text, timeout }) {
    const popupContainer = $(".popupDiv")

    if (popupContainer.length == 0) {
        $("body").append(
            $("<div>", {
                class: "popupDiv"
            })
        )
    }

    const popup = $("<div>", {
        class: `popup ${status}`,
    }).append(
        $("<span>", {
            text: text
        })
    )
        .append(
            $("<span>", {
                class: "close",
                text: "x"
            }).click(function () {
                $(this).parent().remove()
            })
        )

    $(".popupDiv").append(popup)

    if (timeout) {
        setTimeout(() => {
            popup.fadeOut();
        }, timeout);
    }

}

function checkPopup() {
    let popups = localStorage.getItem("popup");
    if (popups) {
        popups = JSON.parse(popups);

        for (let i in popups) {
            createPopup(popups[i]);
        }
        localStorage.removeItem("popup");
    }
}