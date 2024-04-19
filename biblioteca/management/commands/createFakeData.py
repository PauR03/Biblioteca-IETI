import random
from datetime import datetime
from django.core.management.base import BaseCommand
from biblioteca.models import *
from faker import Faker

BOOKS = [
  {
    "titol": "El ingenioso hidalgo Don Quijote de la Mancha",
    "descripcio": "Novela escrita por Miguel de Cervantes Saavedra",
    "autor": "Miguel de Cervantes Saavedra",
    "data_edicio": "16/01/1605",
    "cdu": "863",
    "isbm": "9788424117869",
    "editorial": "Espasa",
    "colleccio": "Clásicos de la literatura",
    "pagines": "1056",
    "signatura": "863CER"
  },
  {
    "titol": "Cien años de soledad",
    "descripcio": "Novela escrita por Gabriel García Márquez",
    "autor": "Gabriel García Márquez",
    "data_edicio": "30/05/1967",
    "cdu": "863",
    "isbm": "9780307474728",
    "editorial": "Cien años de soledad",
    "colleccio": "Realismo mágico",
    "pagines": "432",
    "signatura": "863GAR"
  },
  {
    "titol": "La sombra del viento",
    "descripcio": "Novela escrita por Carlos Ruiz Zafón",
    "autor": "Carlos Ruiz Zafón",
    "data_edicio": "17/04/2001",
    "cdu": "863",
    "isbm": "9788408079545",
    "editorial": "Planeta",
    "colleccio": "El cementerio de los libros olvidados",
    "pagines": "672",
    "signatura": "863ZAF"
  },
  {
    "titol": "Donde los árboles cantan",
    "descripcio": "Novela escrita por Laura Gallego García",
    "autor": "Laura Gallego García",
    "data_edicio": "01/02/2011",
    "cdu": "863",
    "isbm": "9788467577823",
    "editorial": "Montena",
    "colleccio": "Nocturna",
    "pagines": "512",
    "signatura": "863GAL"
  },
  {
    "titol": "La catedral del mar",
    "descripcio": "Novela escrita por Ildefonso Falcones",
    "autor": "Ildefonso Falcones",
    "data_edicio": "03/10/2006",
    "cdu": "863",
    "isbm": "9788425336517",
    "editorial": "Grijalbo",
    "colleccio": "Éxitos",
    "pagines": "704",
    "signatura": "863FAL"
  },
   {
    "titol": "1984",
    "descripcio": "Novela de ficción distópica que presenta un futuro totalitario donde el Gran Hermano todo lo ve y controla",
    "autor": "George Orwell",
    "data_edicio": "08/06/1949",
    "cdu": "84-312",
    "isbm": "9788499890944",
    "editorial": "Debolsillo",
    "colleccio": "Contemporánea",
    "pagines": "368",
    "signatura": "84-312-ORW"
  },
  {
    "titol": "Harry Potter y la piedra filosofal",
    "descripcio": "Primer libro de la saga de Harry Potter, que narra las aventuras del famoso mago durante su primer año en el Colegio Hogwarts de Magia y Hechicería",
    "autor": "J.K. Rowling",
    "data_edicio": "26/06/1997",
    "cdu": "82-312",
    "isbm": "9788478884957",
    "editorial": "Salamandra",
    "colleccio": "Harry Potter",
    "pagines": "256",
    "signatura": "82-312-ROW"
  },
  {
    "titol": "El Gran Gatsby",
    "descripcio": "Novela que explora los temas de la decadencia, el idealismo, la resistencia al cambio social y el exceso",
    "autor": "F. Scott Fitzgerald",
    "data_edicio": "10/04/1925",
    "cdu": "82-312",
    "isbm": "978-3-16-148410-0",
    "editorial": "Charles Scribner's Sons",
    "colleccio": "-",
    "pagines": "180",
    "signatura": "82-312FIT"
  },
  {
    "titol": "Matar a un ruiseñor",
    "descripcio": "Novela que aborda temas como la injusticia racial y la pérdida de la inocencia",
    "autor": "Harper Lee",
    "data_edicio": "11/07/1960",
    "cdu": "84-23",
    "isbm": "978-84-663-4723-7",
    "editorial": "J. B. Lippincott & Co.",
    "colleccio": "-",
    "pagines": "376",
    "signatura": "84-23LEE"
  },
   {
    "titol": "El alquimista",
    "descripcio": "Un joven pastor emprende un viaje en busca de un tesoro oculto.",
    "autor": "Paulo Coelho",
    "data_edicio": "01/05/1988",
    "cdu": "821.134.3",
    "isbm": "9788408015828",
    "editorial": "Editorial Planeta",
    "colleccio": "Biblioteca Paulo Coelho",
    "pagines": "208",
    "signatura": "821COE"
  },
  {
    "titol": "Orgullo y prejuicio",
    "descripcio": "La historia de Elizabeth Bennet y Fitzwilliam Darcy, dos personas que deben superar sus prejuicios para poder enamorarse.",
    "autor": "Jane Austen",
    "data_edicio": "28/01/1813",
    "cdu": "821.111",
    "isbm": "9788499899355",
    "editorial": "Editorial Egales",
    "colleccio": "Biblioteca Jane Austen",
    "pagines": "464",
    "signatura": "821AUS"
  },
  {
    "titol": "El amor en los tiempos del cólera",
    "descripcio": "Una historia de amor en un contexto de epidemia",
    "autor": "Gabriel García Márquez",
    "data_edicio": "10/01/1985",
    "cdu": "823.914",
    "isbm": "978-84-322-0466-1",
    "editorial": "Literatura Random House",
    "colleccio": "No aplica",
    "pagines": 464,
    "signatura": "823GAR"
  },
  {
    "titol": "El principito",
    "descripcio": "Un niño que viaja por diferentes planetas y descubre el sentido de la vida",
    "autor": "Antoine de Saint-Exupéry",
    "data_edicio": "06/04/1943",
    "cdu": "843.912",
    "isbm": "978-84-670-3486-9",
    "editorial": "Salamandra",
    "colleccio": "No aplica",
    "pagines": 96,
    "signatura": "843SAI"
  }
]

DVDS = [
  {
    "titol": "DVD Title 1",
    "descripcio": "DVD Description 1",
    "autor": "DVD Author 1",
    "data_edicio": "01/01/2020",
    "duracio": "120"
  },
  {
    "titol": "DVD Title 2",
    "descripcio": "DVD Description 2",
    "autor": "DVD Author 2",
    "data_edicio": "02/02/2020",
    "duracio": "90"
  },
  {
    "titol": "DVD Title 3",
    "descripcio": "DVD Description 3",
    "autor": "DVD Author 3",
    "data_edicio": "03/03/2020",
    "duracio": "180"
  },
  {
    "titol": "DVD Title 4",
    "descripcio": "DVD Description 4",
    "autor": "DVD Author 4",
    "data_edicio": "04/04/2020",
    "duracio": "150"
  },
  {
    "titol": "DVD Title 5",
    "descripcio": "DVD Description 5",
    "autor": "DVD Author 5",
    "data_edicio": "05/05/2020",
    "duracio": "120"
  },
  {
    "titol": "DVD Title 6",
    "descripcio": "DVD Description 6",
    "autor": "DVD Author 6",
    "data_edicio": "06/06/2020",
    "duracio": "90"
  },
  {
    "titol": "DVD Title 7",
    "descripcio": "DVD Description 7",
    "autor": "DVD Author 7",
    "data_edicio": "07/07/2020",
    "duracio": "180"
  },
  {
    "titol": "DVD Title 8",
    "descripcio": "DVD Description 8",
    "autor": "DVD Author 8",
    "data_edicio": "08/08/2020",
    "duracio": "150"
  },
  {
    "titol": "DVD Title 9",
    "descripcio": "DVD Description 9",
    "autor": "DVD Author 9",
    "data_edicio": "09/09/2020",
    "duracio": "120"
  },
  {
    "titol": "DVD Title 10",
    "descripcio": "DVD Description 10",
    "autor": "DVD Author 10",
    "data_edicio": "10/10/2020",
    "duracio": "90"
  }
]

CDS = [
  {
    "titol": "CD1",
    "descripcio": "Descripcion del CD1",
    "autor": "Autor del CD1",
    "data_edicio": "01/01/2000",
    "discrografia": "Discrografia del CD1",
    "estil": "Estilo de la musica del CD1",
    "duracio": "60"
  },
  {
    "titol": "CD2",
    "descripcio": "Descripcion del CD2",
    "autor": "Autor del CD2",
    "data_edicio": "02/02/2001",
    "discrografia": "Discrografia del CD2",
    "estil": "Estilo de la musica del CD2",
    "duracio": "45"
  },
  {
    "titol": "CD3",
    "descripcio": "Descripcion del CD3",
    "autor": "Autor del CD3",
    "data_edicio": "03/03/2002",
    "discrografia": "Discrografia del CD3",
    "estil": "Estilo de la musica del CD3",
    "duracio": "55"
  },
  {
    "titol": "CD4",
    "descripcio": "Descripcion del CD4",
    "autor": "Autor del CD4",
    "data_edicio": "04/04/2003",
    "discrografia": "Discrografia del CD4",
    "estil": "Estilo de la musica del CD4",
    "duracio": "50"
  },
  {
    "titol": "CD5",
    "descripcio": "Descripcion del CD5",
    "autor": "Autor del CD5",
    "data_edicio": "05/05/2004",
    "discrografia": "Discrografia del CD5",
    "estil": "Estilo de la musica del CD5",
    "duracio": "70"
  },
  {
    "titol": "CD6",
    "descripcio": "Descripcion del CD6",
    "autor": "Autor del CD6",
    "data_edicio": "06/06/2005",
    "discrografia": "Discrografia del CD6",
    "estil": "Estilo de la musica del CD6",
    "duracio": "65"
  },
  {
    "titol": "CD7",
    "descripcio": "Descripcion del CD7",
    "autor": "Autor del CD7",
    "data_edicio": "07/07/2006",
    "discrografia": "Discrografia del CD7",
    "estil": "Estilo de la musica del CD7",
    "duracio": "75"
  },
  {
    "titol": "CD8",
    "descripcio": "Descripcion del CD8",
    "autor": "Autor del CD8",
    "data_edicio": "08/08/2007",
    "discrografia": "Discrografia del CD8",
    "estil": "Estilo de la musica del CD8",
    "duracio": "80"
  },
  {
    "titol": "CD9",
    "descripcio": "Descripcion del CD9",
    "autor": "Autor del CD9",
    "data_edicio": "09/09/2008",
    "discrografia": "Discrografia del CD9",
    "estil": "Estilo de la musica del CD9",
    "duracio": "90"
  },
  {
    "titol": "CD10",
    "descripcio": "Descripcion del CD10",
    "autor": "Autor del CD10",
    "data_edicio": "10/10/2009",
    "discrografia": "Discrografia del CD10",
    "estil": "Estilo de la musica del CD10",
    "duracio": "100"
  }
]

BLUERAYS = [
  {
    "titol": "Avengers: Endgame",
    "descripcio": "La culminación de 22 películas interconectadas, el cuarto capítulo de la saga Avengers atraerá a las audiencias a presenciar el punto de inflexión de este viaje épico. Nuestros queridos héroes comprenderán realmente cuán frágil es esta realidad y los sacrificios que deben hacerse para mantenerla.",
    "autor": "Anthony Russo, Joe Russo",
    "data_edicio": "26/04/2019",
    "duracio": "181"
  },
  {
    "titol": "The Lion King",
    "descripcio": "Simba idolatra a su padre, el rey Mufasa, y está entusiasmado con su destino real. Pero no todos en el reino celebran la llegada del nuevo cachorro. Scar, el hermano de Mufasa y antiguo heredero al trono, tiene sus propios planes.",
    "autor": "Jon Favreau",
    "data_edicio": "19/07/2019",
    "duracio": "118"
  },
  {
    "titol": "Joker",
    "descripcio": "Arthur Fleck es un hombre ignorado por la sociedad, cuya motivación en la vida es hacer reír. Pero una serie de trágicos acontecimientos le llevan a ver el mundo de otra forma. Película basada en el popular personaje de DC Comics Joker, conocido como archienemigo de Batman.",
    "autor": "Todd Phillips",
    "data_edicio": "04/10/2019",
    "duracio": "122"
  },
  {
    "titol": "Frozen II",
    "descripcio": "Por fin ha llegado el esperado día en el que Elsa, Anna, Kristoff y Olaf abandonan Arendelle para viajar hasta un lejano y antiguo bosque de una tierra encantada. Allí encontrarán no sólo a Elsa, sino también respuestas a preguntas que siempre se ha hecho.",
    "autor": "Jennifer Lee, Chris Buck",
    "data_edicio": "22/11/2019",
    "duracio": "103"
  },
  {
    "titol": "Spider-Man: Far From Home",
    "descripcio": "Peter Parker decide irse junto a MJ, Ned y el resto de sus amigos a pasar unas vacaciones a Europa. Sin embargo, el plan de Parker por dejar de lado sus superpoderes durante unas semanas se ven truncados cuando Nick Fury lo contacta para solicitarle ayuda para frenar el ataque de unas criaturas elementales que están causando el caos en el continente.",
    "autor": "Jon Watts",
    "data_edicio": "05/07/2019",
    "duracio": "129"
  },
  {
    "titol": "Toy Story 4",
    "descripcio": "Woody siempre ha tenido claro cuál es su labor en el mundo y cuál es su prioridad: cuidar a su dueño, ya sea Andy o Bonnie. Pero cuando Bonnie añade a Forky, un nuevo juguete de fabricación propia a su habitación, arranca una nueva aventura que servirá para que los viejos y nuevos amigos le enseñen a Woody lo grande que puede ser el mundo si eres un juguete.",
    "autor": "Josh Cooley",
    "data_edicio": "21/06/2019",
    "duracio": "100"
  },
  {
    "titol": "The Dark Knight",
    "descripcio": "Batman regresa para continuar su guerra contra el crimen. Con la ayuda del teniente Jim Gordon y el Fiscal del Distrito Harvey Dent, Batman tiene como objetivo destruir el crimen organizado en la ciudad de Gotham. El triunvirato demuestra ser eficaz, pero pronto termina siendo presa del caos desencadenado por una mente criminal en auge conocida como Joker.",
    "autor": "Christopher Nolan",
    "data_edicio": "18/07/2008",
    "duracio": "152"
  },
  {
    "titol": "Inception",
    "descripcio": "Dom Cobb es un ladrón hábil, el mejor en el peligroso arte de la extracción: robar valiosos secretos del subconsciente durante el estado de sueño cuando la mente está más vulnerable. Esta habilidad excepcional de Cobb le ha hecho un jugador codiciado en el traicionero nuevo mundo de espionaje corporativo, pero también le ha convertido en un fugitivo internacional.",
    "autor": "Christopher Nolan",
    "data_edicio": "16/07/2010",
    "duracio": "148"
  },
  {
    "titol": "Interstellar",
    "descripcio": "Un grupo de exploradores aprovecha un agujero de gusano recién descubierto para superar las limitaciones de los viajes espaciales tripulados y vencer las inmensas distancias que tiene un viaje interestelar.",
    "autor": "Christopher Nolan",
    "data_edicio": "07/11/2014",
    "duracio": "169"
  },
  {
    "titol": "The Matrix",
    "descripcio": "Un hacker llamado Neo descubre que toda su vida ha sido una ilusión, creada por una inteligencia artificial que domina el mundo.",
    "autor": "Lana Wachowski, Lilly Wachowski",
    "data_edicio": "31/03/1999",
    "duracio": "136"
  }
]

DISPOSITIUS = [
  {
    "titol": "Apple iPod",
    "descripcio": "Reproductor de música y video portátil",
    "autor": "Apple Inc.",
    "data_edicio": "23/10/2001",
    "marca": "Apple",
    "model": "iPod"
  },
  {
    "titol": "Sony Walkman",
    "descripcio": "Reproductor de música portátil",
    "autor": "Sony Corporation",
    "data_edicio": "01/07/1979",
    "marca": "Sony",
    "model": "Walkman"
  },
  {
    "titol": "Microsoft Zune",
    "descripcio": "Reproductor de música y video portátil",
    "autor": "Microsoft Corporation",
    "data_edicio": "14/11/2006",
    "marca": "Microsoft",
    "model": "Zune"
  },
  {
    "titol": "SanDisk Sansa",
    "descripcio": "Reproductor de música portátil",
    "autor": "SanDisk Corporation",
    "data_edicio": "20/03/2004",
    "marca": "SanDisk",
    "model": "Sansa"
  },
  {
    "titol": "Creative Zen",
    "descripcio": "Reproductor de música y video portátil",
    "autor": "Creative Technology Ltd.",
    "data_edicio": "17/12/2002",
    "marca": "Creative",
    "model": "Zen"
  },
  {
    "titol": "Samsung Galaxy Player",
    "descripcio": "Reproductor de música y video portátil",
    "autor": "Samsung Electronics Co., Ltd.",
    "data_edicio": "26/09/2010",
    "marca": "Samsung",
    "model": "Galaxy Player"
  },
  {
    "titol": "Archos Jukebox",
    "descripcio": "Reproductor de música portátil",
    "autor": "Archos S.A.",
    "data_edicio": "20/08/2000",
    "marca": "Archos",
    "model": "Jukebox"
  },
  {
    "titol": "iRiver H320",
    "descripcio": "Reproductor de música y video portátil",
    "autor": "iRiver Limited",
    "data_edicio": "09/09/2004",
    "marca": "iRiver",
    "model": "H320"
  },
  {
    "titol": "COWON D2",
    "descripcio": "Reproductor de música y video portátil",
    "autor": "COWON Systems, Inc.",
    "data_edicio": "21/06/2006",
    "marca": "COWON",
    "model": "D2"
  },
  {
    "titol": "Pioneer XDP-100R",
    "descripcio": "Reproductor de música y video portátil",
    "autor": "Pioneer Corporation",
    "data_edicio": "06/11/2015",
    "marca": "Pioneer",
    "model": "XDP-100R"
  }
]

fake = Faker('es_ES')
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crear 2 centros
        Centre.objects.create(nom="Biblioteca IETI")
        Centre.objects.create(nom="Biblioteca Central Cornella")

        # Crear 10 usuarios normales
        for _ in range(10):
            userFirstName=fake.first_name()
            userLastName=fake.last_name()
            User.objects.create_user(
                username=f"{userFirstName}{userLastName}",
                first_name=userFirstName,
                last_name=userLastName,
                email=f"{userFirstName + userLastName}@gmail.com",
                dataNaixement=fake.date_of_birth(minimum_age=13, maximum_age=30),
                centre = Centre.objects.get(pk=random.randint(1, 2)),
                password="P@ssw0rd",
                esAdmin=False
            )

        # Crear 2 usuarios administradores
        User.objects.create_user(
            username="Bibliotecari IETI",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            dataNaixement=fake.date_of_birth(minimum_age=18, maximum_age=65),
            centre = Centre.objects.get(pk=1),
            password="P@ssw0rd",
            esAdmin=True
        )
        User.objects.create_user(
            username="Bibliotecari Central Cornella",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            dataNaixement=fake.date_of_birth(minimum_age=18, maximum_age=65),
            centre = Centre.objects.get(pk=2),
            password="P@ssw0rd",
            esAdmin=True
        )

        # Crear 90 productos
        for book in BOOKS:
            Llibre.objects.create(
                titol=book["titol"],
                descripcio=book["descripcio"],
                autor=book["autor"],
                data_edicio=datetime.strptime(book["data_edicio"], "%d/%m/%Y").date(),
                cdu = book["cdu"],
                isbm = book["isbm"],
                editorial = book["editorial"],
                colleccio = book["colleccio"],
                pagines = book["pagines"],
                signatura = book["signatura"]
            )

        for dvd in DVDS:
            DVD.objects.create(
                titol=dvd["titol"],
                descripcio=dvd["descripcio"],
                autor=dvd["autor"],
                data_edicio=datetime.strptime(dvd["data_edicio"], "%d/%m/%Y").date(),
            )

        for cd in CDS:
            CD.objects.create(
                titol=cd["titol"],
                descripcio=cd["descripcio"],
                autor=cd["autor"],
                data_edicio=datetime.strptime(cd["data_edicio"], "%d/%m/%Y").date(),
                discrografia = cd["discrografia"],
                estil = cd["estil"],
                duracio = cd["duracio"]
            )

        for blueRay in BLUERAYS:
            BR.objects.create(
                titol=blueRay["titol"],
                descripcio=blueRay["descripcio"],
                autor=blueRay["autor"],
                data_edicio=datetime.strptime(blueRay["data_edicio"], "%d/%m/%Y").date(),
                duracio = blueRay["duracio"]
            )

        for dispositiu in DISPOSITIUS:
            Dispositiu.objects.create(
                titol=dispositiu["titol"],
                descripcio=dispositiu["descripcio"],
                autor=dispositiu["autor"],
                data_edicio=datetime.strptime(dispositiu["data_edicio"], "%d/%m/%Y").date(),
                marca = dispositiu["marca"],
                model = dispositiu["model"]
            )

        # Asignar ejemplares a los centros
        productos = Producte.objects.all()
        centros = Centre.objects.all()
        for producte in productos:
            for centre in centros:
                quantitat = random.randint(1, 10)
                Exemplar.objects.create(
                    producte=producte,
                    centre=centre,
                    quantitat=quantitat
                )
        self.stdout.write('Fake data created successfully!')

