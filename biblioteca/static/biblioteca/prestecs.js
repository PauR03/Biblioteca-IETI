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
        success: appendPrestecs,
    })

    $(".createNewPrestec").click(createNewPrestec)
    $(".closePopup").click(closePopup)
    $(".createPrestec").click(createPrestec)

    // Autocompletado y búsqueda de productos
    const awesompleteProductes = new Awesomplete($("#searchInputProducts")[0])
    $("#searchInputProducts").on("keyup", function () {
        const query = $(this).val()
        if (query.length < 3) {
            awesompleteProductes.list = []
            return
        }

        $.ajax({
            url: "/api/autocompletePrestecs/",
            type: 'POST',
            data: { query },
            dataType: 'json',
            success: (data) => awesompleteProductes.list = data
        })
    })

    const awesompleteUsuaris = new Awesomplete($("#searchInputUsers")[0])
    $("#searchInputUsers").on("keyup", function () {
        const query = $(this).val()
        if (query.length < 3) {
            awesompleteUsuaris.list = []
            return
        }

        $.ajax({
            url: "/api/autocompleteUsuaris/",
            type: 'POST',
            data: { query, centreId },
            dataType: 'json',
            success: (data) => awesompleteUsuaris.list = data
        })
    })

    // Add the value of the actual date
    $("#datePrestec").val((new Date().toISOString().split("T")[0]))

    $("#dateDevolucio").attr("min", (new Date().toISOString().split("T")[0]))
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

const appendPrestecs = (response) => {
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