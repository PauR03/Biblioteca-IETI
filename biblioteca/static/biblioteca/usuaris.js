$(document).ready(main)

function main() {

    $.ajax({
        url: '/api/getUsers',
        type: 'GET',
        success: appendUsers,
    })

    function appendUsers(response) {
        const { users } = response

        $(users).each((index, user) => {
            const { id, email, first_name, last_name, esAdmin, is_superuser, centre_nom, imatgePerfil } = user

            $('table.usuaris tbody').append(
                `<tr id=${id}>
                        <td class="imatge">
                            <a href="/perfil/${id}">
                                <img src="/media/${imatgePerfil}" alt="Imatge de perfil">
                            </a>
                        </td>
                        <td class="nom">
                            <a href="/editar_perfil/${id}">
                                ${first_name} ${last_name}
                            </a>
                        </td>
                    <td class="email">${email}</td>
                    <td class="centre">${centre_nom}</td>
                    <td class="rol">${is_superuser ? "Administrador" : esAdmin ? "Bibliotecari" : "Estudiant"}</td>
                </tr>`
            )
        })

        // Esta ultima row se esta añadiendo para tener espacio entre las filas y la tabla no se vea tan pegada al borde
        $('table.usuaris tbody').append("<tr></tr>")
    }
}