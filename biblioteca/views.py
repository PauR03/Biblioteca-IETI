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
        'cicle': cicle,
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
    }
    return render(request, 'producto.html', context)



# APi PARA OBTENER LOS USUARIOS
@login_required
def getUsers(request):
    esSuperUser = request.user.is_superuser
    esBibliotecari = request.user.esAdmin
    centre = request.user.centre

    if esSuperUser:
        users = User.objects.annotate(centre_nom=F('centre__nom')).values('id', 'first_name', 'last_name', 'email', 'centre_nom', 'esAdmin', 'imatgePerfil')
    elif esBibliotecari and centre is not None:
        users = User.objects.filter(centre=centre)
        users = users.annotate(centre_nom=F('centre__nom'))
        users = users.values('id', 'first_name', 'last_name', 'email', 'centre_nom', 'esAdmin', 'imatgePerfil')
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
