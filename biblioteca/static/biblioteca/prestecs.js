$(document).ready(main)

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
    $("#datePrestec").attr("max", (new Date().toISOString().split("T")[0]))


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
        .text("Retornat")
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
                text: esRetornat ? "Retornat" : "No Retornat",
                class: `spanRetornar ${esRetornat ? "retornat" : limitDate ? "limitDate" : "noRetornat"}`

            })
        )

        // Add event listener to the button
        $(".producteRetornat button").last().click((e) => {
            if (!esRetornat) {
                confirmationPopup("Estàs segur que vols continuar?", (respuesta) => {
                    if (respuesta) {
                        const parentTr = $(e.target).closest("tr")
                        const prestecId = parentTr.attr("id")
                        updatePrestec({ prestecId, parentTr })
                    } else return
                })

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
    clearFrom()
}

const createPrestec = async (e) => {
    e.preventDefault()

    const formPrestecData = {
        producte: $("#searchInputProducts").val(),
        userEmail: $("#searchInputUsers").val(),
        dataPrestec: $("#datePrestec").val(),
        dataDevolucio: $("#dateDevolucio").val(),
        centreId,
        adminEmail
    }

    if (!formPrestecData.producte || !formPrestecData.userEmail || !formPrestecData.dataPrestec || !formPrestecData.dataDevolucio) {
        alert("Falten camps per omplir")
        return
    }

    $(".error").each((index, element) => {
        $(element).text("")
        $(element).removeClass("show")
    })

    $.ajax({
        url: '/api/createPrestec/',
        type: 'POST',
        data: formPrestecData,
        success: (response) => successPrestec(response, formPrestecData),
        error: errorPrestec
    })
}

const clearFrom = () => {
    $("#searchInputProducts").val("")
    $("#searchInputUsers").val("")
    $("#datePrestec").val((new Date().toISOString().split("T")[0]))
    $("#dateDevolucio").val("")
    $(".createNewPrestecContainer").addClass("hidden")
}

const successPrestec = (response, formPrestecData) => {
    const { status } = response
    const { prestecId } = response.data

    if (status === "ok") {
        addFirstRow(formPrestecData, prestecId)
        clearFrom()
        createPopup({ status: "success", text: "Prestec creat correctament", timeout: 5000 })
    }
    if (status === "error") {
        createPopup({ status: "error", text: "Error al crear el prestec" })

    }
}

const errorPrestec = (e) => {
    const { responseText, status } = e
    const { message } = JSON.parse(responseText)

    if (status === 404) {
        if (message === "Usuari no trovat") {
            $(".inputUsersError").text(message)
            $(".inputUsersError").addClass("show")
        }
        if (message === "Producte no trovat") {
            $(".inputProductsError").text(message)
            $(".inputProductsError").addClass("show")
        }
        return
    } else if (status === 409) {
        $(".inputsDatesError").text(message)
        $(".inputsDatesError").addClass("show")
        return
    }

    console.error("Error", e)
    alert("Error al crear el prestec")
}

const addFirstRow = (formPrestecData, id) => {

    $('table.prestecs tbody').prepend(
        `<tr id=${id}>
            <td>${formPrestecData.producte}</td>
            <td>${formPrestecData.userEmail}</td>
            <td>${formatDate(formPrestecData.dataPrestec)}</td>
            <td>${formatDate(formPrestecData.dataDevolucio)}</td>
            <td class="retornat"></td>
            <td class="producteRetornat">
                <button>Producte Retornat</button>
            </td>
        </tr>`
    )

    // Add the span element to the last row
    $(".retornat").first().append(
        $("<span>", {
            text: "No Retornat",
            class: `spanRetornar noRetornat`

        })
    )

    // Add event listener to the button
    $(".producteRetornat button").first().click((e) => {
        confirmationPopup("Estàs segur que vols continuar?", (respuesta) => {
            if (respuesta) {
                const parentTr = $(e.target).closest("tr")
                const prestecId = parentTr.attr("id")
                updatePrestec({ prestecId, parentTr })
            } else return
        })
    })
}

function formatDate(dateString) {
    const date = new Date(dateString)
    const day = date.getDate()
    const month = date.getMonth() + 1
    const year = date.getFullYear()
    return `${day}-${month}-${year}`
}

const confirmationPopup = (message, callback) => {
    $("body").append(
        $("<div>", {
            class: "confirmationPopup"
        }).append(
            $("<main>").append(
                $("<p>", {
                    text: message
                })
            ).append(
                $("<footer>").append(
                    $("<button>", {
                        text: "Acceptar",
                        class: "acceptButton",
                        click: () => {
                            $(".confirmationPopup").remove()
                            callback(true)
                        }
                    })
                ).append(
                    $("<button>", {
                        text: "Cancel·la",
                        class: "cancelButton",
                        click: () => {
                            $(".confirmationPopup").remove()
                            callback(false)
                        }
                    })
                )
            )
        )
    )
}