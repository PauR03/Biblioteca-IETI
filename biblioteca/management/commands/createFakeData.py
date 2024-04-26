import random
from datetime import datetime
from django.core.management.base import BaseCommand
from biblioteca.models import *
from faker import Faker

import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

BOOKS = [
  {
    "titol": "El ingenioso hidalgo Don Quijote de la Mancha",
    "descripcio": "Novela escrita por Miguel de Cervantes Saavedra",
    "autor": "Miguel de Cervantes Saavedra",
    "data_edicio": "16/01/1605",
    "cdu": "863",
    "isbn": "9788424117869",
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
    "isbn": "9780307474728",
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
    "isbn": "9788408079545",
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
    "isbn": "9788467577823",
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
    "isbn": "9788425336517",
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
    "isbn": "9788499890944",
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
    "isbn": "9788478884957",
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
    "isbn": "9783161484100",
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
    "isbn": "9788466347237",
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
    "isbn": "9788408015828",
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
    "isbn": "9788499899355",
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
    "isbn": "9788432204661",
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
    "isbn": "9788467034869",
    "editorial": "Salamandra",
    "colleccio": "No aplica",
    "pagines": 96,
    "signatura": "843SAI"
  }
]

DVDS = [
  {
    "titol": "The Shawshank Redemption",
    "descripcio": "Un drama carcelario basado en una historia corta de Stephen King",
    "autor": "Frank Darabont",
    "data_edicio": "14/10/1994",
    "duracio": "142"
  },
  {
    "titol": "The Godfather",
    "descripcio": "Un clásico del cine de mafia dirigido por Francis Ford Coppola",
    "autor": "Francis Ford Coppola",
    "data_edicio": "24/03/1972",
    "duracio": "175"
  },
  {
    "titol": "The Dark Knight",
    "descripcio": "Una película de superhéroes dirigida por Christopher Nolan",
    "autor": "Christopher Nolan",
    "data_edicio": "18/07/2008",
    "duracio": "152"
  },
  {
    "titol": "Pulp Fiction",
    "descripcio": "Una película de crimen y comedia dirigida por Quentin Tarantino",
    "autor": "Quentin Tarantino",
    "data_edicio": "14/10/1994",
    "duracio": "154"
  },
  {
    "titol": "The Lord of the Rings: The Return of the King",
    "descripcio": "La tercera entrega de la trilogía de El Señor de los Anillos dirigida por Peter Jackson",
    "autor": "Peter Jackson",
    "data_edicio": "17/12/2003",
    "duracio": "201"
  },
  {
    "titol": "Schindler's List",
    "descripcio": "Una película histórica basada en la historia real de Oskar Schindler durante el Holocausto",
    "autor": "Steven Spielberg",
    "data_edicio": "15/12/1993",
    "duracio": "195"
  },
  {
    "titol": "Fight Club",
    "descripcio": "Una película de culto dirigida por David Fincher",
    "autor": "David Fincher",
    "data_edicio": "15/10/1999",
    "duracio": "139"
  },
  {
    "titol": "Forrest Gump",
    "descripcio": "Una película dramática dirigida por Robert Zemeckis",
    "autor": "Robert Zemeckis",
    "data_edicio": "06/07/1994",
    "duracio": "142"
  },
  {
    "titol": "Inception",
    "descripcio": "Una película de ciencia ficción dirigida por Christopher Nolan",
    "autor": "Christopher Nolan",
    "data_edicio": "16/07/2010",
    "duracio": "148"
  },
  {
    "titol": "The Matrix",
    "descripcio": "Una película de ciencia ficción y acción dirigida por los hermanos Wachowski",
    "autor": "Lana Wachowski, Lilly Wachowski",
    "data_edicio": "31/03/1999",
    "duracio": "136"
  }
]

CDS = [
  {
    "titol": "Nevermind",
    "descripcio": "El segundo álbum de estudio de la banda de rock Nirvana",
    "autor": "Nirvana",
    "data_edicio": "24/09/1991",
    "discrografia": "DGC Records",
    "estil": "Grunge",
    "duracio": "59"
  },
  {
    "titol": "The Dark Side of the Moon",
    "descripcio": "El octavo álbum de estudio de la banda británica Pink Floyd",
    "autor": "Pink Floyd",
    "data_edicio": "01/03/1973",
    "discrografia": "Harvest Records",
    "estil": "Rock progresivo",
    "duracio": "42"
  },
  {
    "titol": "Thriller",
    "descripcio": "El sexto álbum de estudio del cantante estadounidense Michael Jackson",
    "autor": "Michael Jackson",
    "data_edicio": "30/11/1982",
    "discrografia": "Epic Records",
    "estil": "Pop, R&B",
    "duracio": "42"
  },
  {
    "titol": "Abbey Road",
    "descripcio": "El undécimo álbum de estudio de la banda británica The Beatles",
    "autor": "The Beatles",
    "data_edicio": "26/09/1969",
    "discrografia": "Apple Records",
    "estil": "Rock",
    "duracio": "47"
  },
  {
    "titol": "Back in Black",
    "descripcio": "El séptimo álbum de estudio de la banda australiana de hard rock AC/DC",
    "autor": "AC/DC",
    "data_edicio": "25/07/1980",
    "discrografia": "Atlantic Records",
    "estil": "Hard rock",
    "duracio": "42"
  },
  {
    "titol": "Rumours",
    "descripcio": "El undécimo álbum de estudio de la banda británico-estadounidense Fleetwood Mac",
    "autor": "Fleetwood Mac",
    "data_edicio": "04/02/1977",
    "discrografia": "Warner Bros. Records",
    "estil": "Rock",
    "duracio": "39"
  },
  {
    "titol": "The Wall",
    "descripcio": "El undécimo álbum de estudio de la banda británica Pink Floyd",
    "autor": "Pink Floyd",
    "data_edicio": "30/11/1979",
    "discrografia": "Harvest Records",
    "estil": "Rock progresivo",
    "duracio": "81"
  },
  {
    "titol": "Led Zeppelin IV",
    "descripcio": "El cuarto álbum de estudio de la banda británica Led Zeppelin",
    "autor": "Led Zeppelin",
    "data_edicio": "08/11/1971",
    "discrografia": "Atlantic Records",
    "estil": "Hard rock, heavy metal",
    "duracio": "42"
  },
  {
    "titol": "American Idiot",
    "descripcio": "El séptimo álbum de estudio de la banda estadounidense Green Day",
    "autor": "Green Day",
    "data_edicio": "21/09/2004",
    "discrografia": "Reprise Records",
    "estil": "Punk rock",
    "duracio": "57"
  },
  {
    "titol": "Back to Black",
    "descripcio": "El segundo álbum de estudio de la cantante británica Amy Winehouse",
    "autor": "Amy Winehouse",
    "data_edicio": "27/10/2006",
    "discrografia": "Island Records",
    "estil": "Soul, R&B",
    "duracio": "34"
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

fake = Faker(['es_ES', 'es_CA'])
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crear 2 centros
        if not Centre.objects.filter(nom="Biblioteca IETI").exists() and not Centre.objects.filter(nom="Biblioteca Central Cornella").exists():
          Centre.objects.create(nom="Biblioteca IETI")
          Centre.objects.create(nom="Biblioteca Central Cornella")
          print("Centres created successfully!")

        # Crear 2 usuarios administradores
        if(not User.objects.filter(username="Bibliotecari IETI").exists()):
          User.objects.create_user(
              username="Bibliotecari IETI",
              first_name=fake.first_name(),
              last_name=fake.last_name(),
              email=fake.email(),
              dataNaixement=fake.date_of_birth(minimum_age=18, maximum_age=65),
              centre = Centre.objects.get(pk=1),
              password=env('SEEDER_USERS_PASSWORD'),
              esAdmin=True
          )
          print("Admin users created \"Bibliotecari IETI\"")


        if(not User.objects.filter(username="Bibliotecari Central Cornella").exists()):
          User.objects.create_user(
              username="Bibliotecari Central Cornella",
              first_name=fake.first_name(),
              last_name=fake.last_name(),
              email=fake.email(),
              dataNaixement=fake.date_of_birth(minimum_age=18, maximum_age=65),
              centre = Centre.objects.get(pk=2),
              password=env('SEEDER_USERS_PASSWORD'),
              esAdmin=True
          )
          print("Admin users created \"Bibliotecari Central Cornella\"")

        # Crear 190 productos
        for book in BOOKS:
            if not Llibre.objects.filter(titol=book["titol"]).exists():
              Llibre.objects.create(
                  titol=book["titol"],
                  descripcio=book["descripcio"],
                  autor=book["autor"],
                  data_edicio=datetime.strptime(book["data_edicio"], "%d/%m/%Y").date(),
                  cdu = book["cdu"],
                  isbn = book["isbn"],
                  editorial = book["editorial"],
                  colleccio = book["colleccio"],
                  pagines = book["pagines"],
                  signatura = book["signatura"]
              )
              print(f"Book {book['titol']} created")

        for i in range(100):
            llibreTitol = fake.sentence(nb_words=3)
            Llibre.objects.create(
              titol=llibreTitol,
              descripcio=fake.sentence(nb_words=100),
              autor=fake.name(),
              data_edicio=fake.date_between(start_date='-100y', end_date='today'),
              cdu=fake.random_int(min=100, max=999),
              isbn=fake.isbn13(separator=""),
              editorial=fake.company(),
              colleccio=fake.word(),
              pagines=fake.random_int(min=100, max=500),
              signatura=fake.lexify(text="???-###")
            )
            print(f"Book {llibreTitol} created")

        for dvd in DVDS:
            if not DVD.objects.filter(titol=dvd["titol"]).exists():
              DVD.objects.create(
                  titol=dvd["titol"],
                  descripcio=dvd["descripcio"],
                  autor=dvd["autor"],
                  data_edicio=datetime.strptime(dvd["data_edicio"], "%d/%m/%Y").date(),
                  duracio = dvd["duracio"]
              )
              print(f"DVD {dvd['titol']} created")

        for cd in CDS:
            if not CD.objects.filter(titol=cd["titol"]).exists():
              CD.objects.create(
                titol=cd["titol"],
                descripcio=cd["descripcio"],
                autor=cd["autor"],
                data_edicio=datetime.strptime(cd["data_edicio"], "%d/%m/%Y").date(),
                discrografia=cd["discrografia"],
                estil=cd["estil"],
                duracio=cd["duracio"]
              )
              print(f"CD {cd['titol']} created")

        for blueRay in BLUERAYS:
            if not BR.objects.filter(titol=blueRay["titol"]).exists():
              BR.objects.create(
                  titol=blueRay["titol"],
                  descripcio=blueRay["descripcio"],
                  autor=blueRay["autor"],
                  data_edicio=datetime.strptime(blueRay["data_edicio"], "%d/%m/%Y").date(),
                  duracio = blueRay["duracio"]
              )
              print(f"BR {blueRay['titol']} created")

        for dispositiu in DISPOSITIUS:
            if not Dispositiu.objects.filter(titol=dispositiu["titol"]).exists():
              Dispositiu.objects.create(
                  titol=dispositiu["titol"],
                  descripcio=dispositiu["descripcio"],
                  autor=dispositiu["autor"],
                  data_edicio=datetime.strptime(dispositiu["data_edicio"], "%d/%m/%Y").date(),
                  marca = dispositiu["marca"],
                  model = dispositiu["model"]
              )
              print(f"Dispositiu {dispositiu['titol']} created")

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

        # Crear 10 usuarios normales
        for i in range(10):
            userFirstName=fake.first_name()
            userLastName=fake.last_name()
            newUser = User.objects.create_user(
                username=f"{userFirstName}{userLastName}",
                first_name=userFirstName,
                last_name=userLastName,
                email=f"{userFirstName + userLastName}@gmail.com",
                dataNaixement=fake.date_of_birth(minimum_age=13, maximum_age=30),
                centre = Centre.objects.get(pk=random.randint(1, 2)),
                password=env('SEEDER_USERS_PASSWORD'),
                esAdmin=False
            )
            newUser.save()
            print(f"User {userFirstName} {userLastName} created")

            if i >= 0 and i <= 3:
              randomProducte = Producte.objects.get(pk=random.randint(1, Producte.objects.count()))
              quantitatExemplars = Exemplar.objects.filter(producte=randomProducte).first().quantitat
              quantitatRealExemplars  = quantitatExemplars - Prestec.objects.filter(producte=randomProducte, esRetornat=False).count()
              if quantitatRealExemplars > 0:
                Prestec.objects.create(
                    producte=randomProducte,
                    centre=Centre.objects.get(pk=1),
                    usuari=newUser,
                    usuariAdmin=User.objects.get(username="Bibliotecari IETI"),
                )
                print(f"Prestec creat per al usuari {newUser.username} del producte {randomProducte.titol}")
        self.stdout.write('Fake data created successfully!')