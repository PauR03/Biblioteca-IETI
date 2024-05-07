from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout
from .backends import EmailBackend
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import *
from .serializers import LogSerializer
from django.db.models import Q, F
from django.views import View
from datetime import datetime
import secrets
import string
from biblioteca.models import User  # Importa tu modelo de usuario personalizado
from django.core.mail import send_mail
from django.db import IntegrityError
import random
import csv
import io
from django.urls import reverse

# VIEW PARA LOGIN DE USUARIOS
@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        backend = EmailBackend()
        user = backend.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username

            # Guardar un log de inicio de sesión exitoso
            log_data = {
                'tipus': 'info', 
                'informacio': 'Usuario logeado correctamente',
                'ruta': '/dashboard/',
                'usuari': user.pk  
            }
            serializer = LogSerializer(data=log_data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

            return JsonResponse({'redirect': '/dashboard/'})  
        else:
            # handle failed login case
            response = JsonResponse({'error': 'Invalid login credentials'})
            response.status_code = 401  
            return response
    else:
        return render(request, 'index.html')

# VIEW PARA REDIRIGIR AL USUARIO AL DASHBOARD CON EL TOKEN CSRF
@login_required
def dashboard_view(request):
    email = request.session.get('username')  
    token = request.session.get('token')
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        is_superuser = user.is_superuser
        is_admin = user.esAdmin
        username = user.username  
        firstname = user.first_name  
        lastname = user.last_name  
    except User.DoesNotExist:
        is_superuser = False
        is_admin = False
        username = None  
        firstname = None  
        lastname = None  
        
    return render(request, 'dashboard.html', {'username': username, 'token': token, 'is_superuser': is_superuser, 'is_admin': is_admin, 'firstname': firstname, 'lastname': lastname})

# VIEW PARA HACER LOGOUT
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'ok'})

# VIEW PARA EL PERFIL DEL USUARIO
@login_required
def profile(request):
    # Obtén el usuario actual
    user = request.user

    # Puedes acceder a los atributos del usuario, como username y email
    username = user.username
    email = user.email
    firstname = user.first_name  
    lastname = user.last_name  
    dataNaixement = user.dataNaixement
    cicle = user.cicle
    imatgePerfil = user.imatgePerfil.url if user.imatgePerfil else None

    # Verifica si el usuario es un superusuario o un administrador
    is_superuser = user.is_superuser
    is_admin = user.esAdmin  

    # Pasa estos datos al contexto del template
    context = {
        'username': username,
        'email': email,
        'is_superuser': is_superuser,
        'is_admin': is_admin,
        'dataNaixement': dataNaixement,
        'cicle': "No Definit" if cicle is None else cicle,
        'imatgePerfil': imatgePerfil,
        'firstname': firstname, 
        'lastname': lastname,
        }

    # Renderiza el template con este contexto
    return render(request, 'perfil.html', context)

# ENVIA LOS DATOS DEL USAURIO AL FICHERO EDITAR PERFIL
@login_required
def edit_profile(request):
    user = request.user
    username = user.username
    firstname = user.first_name  # Fetch the first name from the User model
    lastname = user.last_name  # Fetch the last name from the User model
    is_admin = user.esAdmin  # Check if the user is a superuser or if user.esAdmin is True
    is_superuser = user.is_superuser

    context = {
        'username': username,
        'firstname': firstname,  # Add first name to the context
        'lastname': lastname,  # Add last name to the context
        'email': user.email,
        'is_admin': is_admin,
        'is_superuser': is_superuser,
        'dataNaixement': user.dataNaixement,  # Assuming the User model has a dataNaixement field
        'cicle': user.cicle,  # Assuming the User model has a cicle field
    }
    return render(request, 'editarPerfil.html', context)


# HACE EL INSERT DE LOS DATOS MODIFICADOS DEL USUARIO
@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        dataNaixement = request.POST.get('dataNaixement', '')
        cicle = request.POST.get('cicle', '')
        profile_image = request.FILES.get('profile_image', None)
        new_password = request.POST.get('new_password', '')
        confirm_new_password = request.POST.get('confirm_new_password', '')

        user = request.user
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.email = email if email else user.email
        user.dataNaixement = dataNaixement if dataNaixement else user.dataNaixement
        user.cicle = cicle if cicle else user.cicle

        if new_password and new_password == confirm_new_password:
            user.set_password(new_password)
        else:
            messages.error(request, 'Las contraseñas no coinciden')

        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            user.imatgePerfil = filename

        user.save()

        messages.success(request, 'Perfil actualizado con éxito')
        return redirect('editar_perfil')  #SI ES CORRECTO LLAMA A LA VIEW "PROFILE" QUE ESTA REDIRIGE A "PERFIL.HTML" PASANDOLE TODOS LOS DATOS DEL USUARIO

    else:
        return render(request, 'editarPerfil.html')

# BUSCA LA IMAGEN DE PERFIL QUE TIENE EL USUARIO
@login_required
def get_profile_image(request):
    user = request.user
    imatgePerfil = user.imatgePerfil.url if user.imatgePerfil else None
    return JsonResponse({'imatgePerfil': imatgePerfil})

# GUARDAR LOGS EN LA BASE DE DATOS
@api_view(['POST'])
def create_log(request):
    logs = request.data
    responses = []
    for log in logs:
        try:
            # Buscar el usuario por su nombre de usuario
            user = User.objects.get(username=log['usuari'])
            log['usuari'] = user.pk  # Asignar el valor de clave primaria del usuario
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

        serializer = LogSerializer(data=log)
        if serializer.is_valid():
            serializer.save()
            responses.append(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    return Response(responses, status=201)

@login_required
def usuaris_view(request):
    user = request.user
    if not user.is_superuser and not user.esAdmin:
        return redirect('dashboard')
    username = user.username
    firstname = user.first_name  # Fetch the first name from the User model
    lastname = user.last_name  # Fetch the last name from the User model
    is_admin = user.esAdmin  # Check if the user is a superuser or if user.esAdmin is True
    is_superuser = user.is_superuser

    context = {
        'username': username,
        'firstname': firstname,  # Add first name to the context
        'lastname': lastname,  # Add last name to the context
        'email': user.email,
        'is_admin': is_admin,
        'is_superuser': is_superuser,
        'dataNaixement': user.dataNaixement,  # Assuming the User model has a dataNaixement field
        'cicle': user.cicle,  # Assuming the User model has a cicle field
    }
    return render(request, 'usuaris.html', context)

# BUSCADOR 'LANDINGPAGE'
class AutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        available_only = request.GET.get('available_only', 'false') == 'true'
        if len(query) < 3:
            return JsonResponse([], safe=False)
        productes = Producte.objects.filter(Q(titol__icontains=query) | Q(autor__icontains=query))
        if available_only:
            for producte in productes:
                    quantitatExemplars = Exemplar.objects.filter(producte=producte).first().quantitat
                    quantitatPrestecsNoRetornats = Prestec.objects.filter(producte=producte, esRetornat=False).count()
                    quantitatRealExemplars = quantitatExemplars - quantitatPrestecsNoRetornats
                    if quantitatRealExemplars <= 0:
                        productes = productes.exclude(id=producte.id)
        productes = productes[:5]
        titols = [producte.titol for producte in productes]
        autors = list(set([producte.autor for producte in productes if producte.autor]))
        suggestions = titols + autors
        return JsonResponse(suggestions, safe=False)
    
# REDIRIGE A LA PAGINA "PRODUCTO.HTML" Y BUSCA LOS PRODUCTOS QUE COINCIDAN CON EL TITULO O AUTOR
def product_detail(request):
    query = request.GET.get('q', '')
    available_only = request.GET.get('available_only', 'false') == 'true'

    if len(query) < 3:
        return redirect('login')
    
    productes = Producte.objects.filter(Q(titol__icontains=query) | Q(autor__icontains=query)).order_by('autor')
    
    if available_only:
        for producte in productes:
            quantitatExemplars = Exemplar.objects.filter(producte=producte).first().quantitat
            quantitatPrestecsNoRetornats = Prestec.objects.filter(producte=producte, esRetornat=False).count()
            quantitatRealExemplars = quantitatExemplars - quantitatPrestecsNoRetornats
            if quantitatRealExemplars <= 0:
                productes = productes.exclude(id=producte.id)

    search_type = 'autor' if Producte.objects.filter(autor__icontains=query).exists() else 'titol'

    context = {
        'productes': productes,
        'search_type': search_type,
        'search_term': query,  # Agregamos el término de búsqueda al contexto
    }
    return render(request, 'producto.html', context)

# APi PARA OBTENER LOS USUARIOS
@login_required
def getUsers(request):
    esSuperUser = request.user.is_superuser
    esBibliotecari = request.user.esAdmin
    centre = request.user.centre

    if esSuperUser:
        users = User.objects.annotate(centre_nom=F('centre__nom')).values('id', 'first_name', 'last_name', 'email', 'centre_nom', 'esAdmin', 'imatgePerfil', 'is_superuser')
    elif esBibliotecari and centre is not None:
        users = User.objects.filter(centre=centre)
        users = users.annotate(centre_nom=F('centre__nom'))
        users = users.values('id', 'first_name', 'last_name', 'email', 'centre_nom', 'esAdmin', 'imatgePerfil', 'is_superuser')
    else:
        users = {}

    return JsonResponse({
        'users': list(users)
    })

# VIEW PARA EDITAR EL PERFIL DEL USUARIO
@login_required
def edit_profile_user(request, id):
    user = request.user
    userToEdit = User.objects.get(pk=id)

    if not user.is_superuser and not user.esAdmin:
        return redirect('dashboard')

    if user.esAdmin and user.centre != userToEdit.centre:
        return redirect('dashboard')

    firstname = user.first_name 
    lastname = user.last_name
    is_admin = user.esAdmin
    is_superuser = user.is_superuser

    dataNaixement = userToEdit.dataNaixement

    context = {
        'firstname': firstname,
        'lastname': lastname,
        'is_admin': is_admin,
        'is_superuser': is_superuser,
        'userToEdit':{
            'id': userToEdit.id,
            'firstname': userToEdit.first_name,
            'lastname': userToEdit.last_name,
            'email': userToEdit.email,
            'dataNaixement': dataNaixement,
            'imatgePerfil': userToEdit.imatgePerfil.url if userToEdit.imatgePerfil else 'imatgePerfil/default.jpg',
        }
    }
    return render(request, 'editarPerfilUsuario.html', context)

@login_required
def update_profile_user(request, id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        dataNaixement = request.POST.get('dataNaixement', '')
        cicle = request.POST.get('cicle', '')
        profile_image = request.FILES.get('profile_image', None)
        new_password = request.POST.get('new_password', '')
        confirm_new_password = request.POST.get('confirm_new_password', '')

        user = User.objects.get(pk=id)
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.email = email if email else user.email
        user.dataNaixement = dataNaixement if dataNaixement else user.dataNaixement
        user.cicle = cicle if cicle else user.cicle

        if new_password and new_password == confirm_new_password:
            user.set_password(new_password)
        else:
            messages.error(request, 'Las contraseñas no coinciden')

        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            user.imatgePerfil = filename

        user.save()
        
        messages.success(request, 'Perfil actualizado con éxito')
        # return redirect('editar_perfil', id=id)  #SI ES CORRECTO LLAMA A LA VIEW "PROFILE" QUE ESTA REDIRIGE A "PERFIL.HTML" PASANDOLE TODOS LOS DATOS DEL USUARIO

        previous_url = request.META.get('HTTP_REFERER')
        if previous_url:
            return redirect(previous_url)
    else:
        return render(request, 'dashboard.html')

@login_required
def prestecs(request):
    user = request.user
    if not user.is_superuser and not user.esAdmin:
        return redirect('dashboard')
    firstname = user.first_name 
    lastname = user.last_name
    is_admin = user.esAdmin
    is_superuser = user.is_superuser

    context = {
        'firstname': firstname,
        'lastname': lastname, 
        'is_admin': is_admin,
        'is_superuser': is_superuser,
    }
    return render(request, 'prestecs.html', context)

# API PARA OBTENER LOS PRESTAMOS
@login_required
def getPrestecs(request):
    user = request.user
    centre = user.centre if user.centre else 1

    prestecs = Prestec.objects.filter(centre=centre)
    prestecs = prestecs.values('id', 'dataPrestec', 'dataDevolucio', 'producte__titol', 'usuari__email', 'esRetornat').order_by('-dataPrestec')

    return JsonResponse({
        'prestecs': list(prestecs)
    })

# API PARA ACTUALIZAR LOS PRESTAMOS
@api_view(['POST'])
def updatePrestec(request):
    try:
        prestecId = request.data['prestecId']
        prestec = Prestec.objects.get(pk=prestecId)
        prestec.esRetornat = True
        prestec.save()
        return Response({'status': 'ok'}, status=200)
    except:
        return Response({'status': 'error'}, status=400)

# BUSCADOR 'LANDINGPAGE'
@api_view(['POST'])
def autocompletePrestecs(request):
    query = request.data.get('query', '')
    if len(query) < 3:
        return JsonResponse([], safe=False)
    
    productes = Producte.objects.filter(Q(titol__icontains=query))

    for producte in productes:
            quantitatExemplars = Exemplar.objects.filter(producte=producte).first().quantitat
            quantitatPrestecsNoRetornats = Prestec.objects.filter(producte=producte, esRetornat=False).count()
            quantitatRealExemplars = quantitatExemplars - quantitatPrestecsNoRetornats
            if quantitatRealExemplars <= 0:
                productes = productes.exclude(id=producte.id)
    productes = productes[:5]
    titols = [producte.titol for producte in productes]
    suggestions = titols
    
    return JsonResponse(suggestions, safe=False)

# BUSCADOR 'LANDINGPAGE'
@api_view(['POST'])
def autocompleteUsuaris(request):
    userEmail = request.data.get('query', '')
    centreId = request.data.get('centreId', '')

    if len(userEmail) < 3:
        return JsonResponse([], safe=False)
    
    users = User.objects.filter(Q(email__icontains=userEmail), centre=centreId).values('email')
    users = users[:5]
    usersEmail = [user['email'] for user in users]
    
    return JsonResponse(usersEmail, safe=False)

# API PARA CREAR UN PRESTAMO
@api_view(['POST'])
def createPrestec(request):
    try:
        dataPrestec = request.data['dataPrestec']
        dataDevolucio = request.data['dataDevolucio']
        producte = request.data['producte']
        userEmail = request.data['userEmail']
        centreId = request.data['centreId']
        adminEmail = request.data['adminEmail']
        
        try:
            producte = Producte.objects.get(titol=producte)
        except:
            return Response({'status': 'error', 'message': 'Producte no trovat'}, status=404)
    
        try:
            usuari = User.objects.get(email=userEmail)
        except:
            return Response({'status': 'error', 'message': 'Usuari no trovat'}, status=404)

        if(dataDevolucio <= dataPrestec):
            return Response({'status': 'error', 'message': 'La data de devolució ha de ser posterior a la data de préstec'}, status=409)
        centre = Centre.objects.get(pk=centreId)
        adminEmail = User.objects.get(email=adminEmail)

        prestec = Prestec(
            dataPrestec=dataPrestec, 
            dataDevolucio=dataDevolucio, 
            producte=producte, 
            usuari=usuari, 
            centre=centre, 
            usuariAdmin=adminEmail)
        prestec.save()

        prestecId = prestec.id

        return Response({'status': 'ok','data':{'prestecId':prestecId}}, status=200)
    except Exception as e:
        print(e)
        return Response({'status': 'error'}, status=400)

def generate_password():
    # Define the character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Generate a password that contains at least one (lowercase letter, uppercase letter, digit, symbol)
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    # Fill the rest of the password with random characters from all sets
    all_characters = lowercase + uppercase + digits + symbols
    password += [secrets.choice(all_characters) for _ in range(8 - len(password))]

    # Shuffle the password to ensure randomness
    secrets.SystemRandom().shuffle(password)

    # Convert the list to a string
    password = ''.join(password)

    return password




def crear_usuario(request):
    # Obtén el usuario actual
    current_user = request.user

    # Verifica si el usuario actual es un superusuario o un administrador
    is_superuser = current_user.is_superuser
    is_admin = current_user.esAdmin  

    # Pasa estos datos al contexto del template
    context = {
        'is_superuser': is_superuser,
        'is_admin': is_admin,
        'firstname': current_user.first_name,  
        'lastname': current_user.last_name,  
        'imatgePerfil': current_user.imatgePerfil,  
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        base_username = f"{first_name}_{last_name}" if first_name and last_name else None
        username = base_username
        # Genera un nombre de usuario único
        while User.objects.filter(username=username).exists():
            username = base_username + str(random.randint(1, 1000))
        email = request.POST.get('email', None)
        dataNaixement = request.POST.get('dataNaixement', None)
        if dataNaixement == "":
            dataNaixement = None
        cicle = request.POST.get('cicle', None)
        profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None

        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name, profile_image)
            profile_image_url = fs.url(filename)
        else:
            profile_image_url = 'imatgePerfil/default.jpg'

        password = generate_password()

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El correu electrònic ja està en ús'}, status=400)
        else:
            try:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, dataNaixement=dataNaixement, cicle=cicle, imatgePerfil=profile_image_url, centre=current_user.centre)  # Usa tu propio modelo de usuario
                user.set_password(password)
                user.save()

                try:
                    send_mail(
                        'Benvingut a la biblioteca Mari Carmen Brito',
                        f'Hola {first_name},\n\nLa teva contrasenya és: {password}\n\nSi desitges canviar-la, pots fer-ho en el següent enllaç: https://biblio6.ieti.site/password_reset/\n\n Salutacions.\n',
                        settings.EMAIL_HOST_USER,  # Use the email configured in settings
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f'Error sending email: {e}')
                print(f'Usuario {username} creado con éxito')  # Imprime un mensaje en la consola cuando se crea un usuario

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        messages.success(request, 'Usuario creado con éxito')
        return JsonResponse({'redirect': reverse('crear_usuario')})  # Reemplaza 'crear_usuario' con la URL a la que quieres redirigir
        print(redirect_url)
    return render(request, 'crearUsuario.html', context)

def importar_usuarios(request):
    current_user = request.user
    is_superuser = current_user.is_superuser
    is_admin = current_user.esAdmin  
    centres = Centre.objects.all()

    if request.method == 'POST':
        errors = []
        successes = []  # Agregamos una lista para los mensajes de éxito
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            errors.append('L\'arxiu ha de ser un full de calcul (.csv)')
            return JsonResponse({'errors': errors})

        try:
            data_set = csv_file.read().decode('ISO-8859-1')
        except UnicodeDecodeError:
            errors.append('El fitxer CSV ha d\'estar codificat com a ISO-8859-1.')
            return JsonResponse({'errors': errors})

        data_set = data_set.replace('\r\n', '\n').replace('\r', '\n')
        io_string = io.StringIO(data_set)
        next(io_string)

        centre_id = request.POST['centre_id']
        centre = Centre.objects.get(id=centre_id)

        emails = set()
        phones = set()

        for line_number, column in enumerate(csv.reader(io_string, delimiter=','), start=1):
            if len(column) >= 5:  # Cambiado de 6 a 5
                if not column[0] or not column[1] or not column[2] or not column[3] or not column[4]:
                    errors.append(f'A la línia {line_number} falten dades.')
                    continue

                email = column[3]
                phone = column[4]

                if email in emails or phone in phones:
                    errors.append(f'A la línia {line_number}, les dades estan duplicades al CSV.')
                    continue

                emails.add(email)
                phones.add(phone)

                if User.objects.filter(email=email).exists():
                    errors.append(f'A la línia {line_number}, l\'usuari amb el correu electrònic {email} ja hi és enregistrat.')
                    continue

                if User.objects.filter(telefon=phone).exists():
                    errors.append(f'A la línia {line_number}, l\'usuari amb el telèfon {phone} ja hi es enregistrat.')
                    continue

                try:
                    username = f"{column[0]}_{column[1]}_{random.randint(1000, 9999)}"

                    _, created = User.objects.update_or_create(
                        username=username,
                        first_name=column[0],
                        last_name=f"{column[1]} {column[2]}",
                        email=email,
                        telefon=phone,
                        cicle=column[5],
                        centre_id=centre_id
                    )

                    print(created)  # Imprime el valor de created

                    if created:  # Si se creó un nuevo usuario
                        successes.append(f'A la línia {line_number}, l\'usuari {username} s\'ha inserit correctament.')
                except IntegrityError as e:
                    field = 'unknown'
                    if 'email' in str(e):
                        field = 'email'
                    elif 'telefon' in str(e):
                        field = 'telefon'
                    errors.append(f'A la línia {line_number}, el camp {field} ja hi és enregistrat.')
                except Exception as e:
                    errors.append(f'Error a la línia {line_number}: {str(e)}')
            else:
                errors.append(f'La línia {line_number} no té el nombre correcte de columnes.')

        if errors:
            return JsonResponse({'errors': errors})
        else:
            return JsonResponse({'success': 'Archivo subido con éxito', 'successes': successes})  # Devolvemos los mensajes de éxito

    context = {
        'is_superuser': is_superuser,
        'is_admin': is_admin,
        'firstname': current_user.first_name,  
        'lastname': current_user.last_name,  
        'imatgePerfil': current_user.imatgePerfil,  
        'centres': centres,
    }

    return render(request, 'importarUsuarios.html', context)
