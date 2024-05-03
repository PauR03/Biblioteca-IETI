$(document).ready(main)
const formPrestecData = {
    producteId: null,
    usuariId: null,
    dataPrestec: null,
    dataDevolucio: null
}
function main() {

    $.ajax({
        url: '/api/getPrestecs',
        type: 'GET',
        success: appendUsers,
    })

    $(".createNewPrestec").click(createNewPrestec)
    $(".closePopup").click(closePopup)
    $(".createPrestec").click(createPrestec)

    // Autocompletado y búsqueda
    const input = $("#search-input");
    let awesomplete = new Awesomplete(input[0]);
    let searchResults = []

    input.on("keyup", function () {
        const query = this.value
        if (query.length < 3) {
            awesomplete.list = []
            return
        }

        $.ajax({
            url: "/api/autocompletePrestecs/",
            type: 'POST',
            data: {
                'q': query
            },
            dataType: 'json',
            success: function (data) {
                awesomplete.list = data
                searchResults = data.slice(Math.floor(data.length / 2))
                console.log(searchResults)
            }
        })
    })

}

const updatePrestec = async ({ prestecId, parentTr }) => {
    const response = await $.ajax({
        url: '/api/updatePrestec/',
        type: 'POST',
        data: { prestecId },
    })
    const { status } = response

    if (status === "ok") updatePrestecStatusClient({ parentTr })
    if (status === "error") alert("Error al retornar el producte")
}

const updatePrestecStatusClient = ({ parentTr }) => {
    $(parentTr).find(".spanRetornar")
        .text("esRetornat")
        .addClass("retornat")
        .removeClass("noRetornat")

    $(parentTr).find(".producteRetornat button").off("click")
}

const appendUsers = (response) => {
    const { prestecs } = response
    $(prestecs).each((index, prestec) => {
        const { id, dataPrestec, dataDevolucio, producte__titol, usuari__email, esRetornat } = prestec

        $('table.prestecs tbody').append(
            `<tr id=${id}>
                <td>${producte__titol}</td>
                <td>${usuari__email}</td>
                <td>${formatDate(dataPrestec)}</td>
                <td>${formatDate(dataDevolucio)}</td>
                <td class="retornat"></td>
                <td class="producteRetornat">
                    <button>Producte Retornat</button>
                </td>
            </tr>`
        )
        const limitDate = new Date(dataDevolucio) < new Date()

        // Add the span element to the last row
        $(".retornat").last().append(
            $("<span>", {
                text: esRetornat ? "esRetornat" : "noRetornat",
                class: `spanRetornar ${esRetornat ? "retornat" : limitDate ? "limitDate" : "noRetornat"}`

            })
        )

        // Add event listener to the button
        $(".producteRetornat button").last().click((e) => {
            if (!esRetornat) {
                const confirmation = confirm("Estas segur que vols retornar el producte?")
                if (!confirmation) return
                const parentTr = $(e.target).closest("tr")
                const prestecId = parentTr.attr("id")
                updatePrestec({ prestecId, parentTr })
            }
        })
    })

    // Esta ultima row se esta añadiendo para tener espacio entre las filas y la tabla no se vea tan pegada al borde
    $('table.prestecs tbody').append("<tr></tr>")
}

const createNewPrestec = () => {
    $(".createNewPrestecContainer").removeClass("hidden")
}

const closePopup = (e) => {
    e.preventDefault()
    $(".createNewPrestecContainer").addClass("hidden")
}

const createPrestec = async (e) => {
    e.preventDefault()
    console.log("createPrestec")
}

function formatDate(dateString) {
    const date = new Date(dateString)
    const day = date.getDate()
    const month = date.getMonth() + 1
    const year = date.getFullYear()
    return `${day}-${month}-${year}`
}