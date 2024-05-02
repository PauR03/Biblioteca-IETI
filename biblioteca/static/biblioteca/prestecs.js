$(document).ready(main)

function main() {

    $.ajax({
        url: '/api/getPrestecs',
        type: 'GET',
        success: appendUsers,
    })

    function appendUsers(response) {
        const { prestecs } = response
        console.table(prestecs)
        $(prestecs).each((index, prestec) => {
            const { id, dataPrestec, dataDevolucio, producte__titol, usuari__email, esRetornat } = prestec

            $('table.prestecs tbody').append(
                `<tr id=${id}>
                    <td>${producte__titol}</td>
                    <td>${usuari__email}</td>
                    <td>${formatDate(dataPrestec)}</td>
                    <td>${formatDate(dataDevolucio)}</td>
                    <td class="retornat"></td>
                    <td class="producteRetornat"><button>Producte Retornat</button></td>
                </tr>`
            )

            $(".retornat").last().append(
                $("<span>", {
                    text: esRetornat ? "esRetornat" : "noRetornat",
                    class: esRetornat ? "retornat" : "noRetornat"

                })
            )

            $(".producteRetornat").last().click(() => {

            })

        })


        // Esta ultima row se esta añadiendo para tener espacio entre las filas y la tabla no se vea tan pegada al borde
        $('table.prestecs tbody').append("<tr></tr>")
    }
}

function formatDate(dateString) {
    const date = new Date(dateString)
    const day = date.getDate()
    const month = date.getMonth() + 1
    const year = date.getFullYear()
    return `${day}-${month}-${year}`
}