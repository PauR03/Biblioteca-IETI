$(document).ready(main)

function main() {

    $.ajax({
        url: '/api/getPrestecs',
        type: 'GET',
        success: appendUsers,
    })

    function appendUsers(response) {
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

function formatDate(dateString) {
    const date = new Date(dateString)
    const day = date.getDate()
    const month = date.getMonth() + 1
    const year = date.getFullYear()
    return `${day}-${month}-${year}`
}