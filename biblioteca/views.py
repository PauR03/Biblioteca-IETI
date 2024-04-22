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
        is_admin = user.is_superuser or user.esAdmin
        username = user.username  # Fetch the username from the User model
        firstname = user.first_name  # Fetch the first name from the User model
        lastname = user.last_name  # Fetch the last name from the User model
    except User.DoesNotExist:
        is_admin = False
        username = None  # Set username to None if the user does not exist
        firstname = None  # Set first name to None if the user does not exist
        lastname = None  # Set last name to None if the user does not exist
    return render(request, 'dashboard.html', {'username': username, 'token': token, 'is_admin': is_admin, 'firstname': firstname, 'lastname': lastname})




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
    firstname = user.first_name  # Fetch the first name from the User model
    lastname = user.last_name  # Fetch the last name from the User model
    dataNaixement = user.dataNaixement
    cicle = user.cicle
    imatgePerfil = user.imatgePerfil.url if user.imatgePerfil else None

    # También puedes verificar si el usuario es un administrador
    is_admin = user.is_superuser

    # Pasa estos datos al contexto del template
    context = {
        'username': username,
        'email': email,
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
    is_admin = user.is_superuser

    context = {
        'username': username,
        'firstname': firstname,  # Add first name to the context
        'lastname': lastname,  # Add last name to the context
        'email': user.email,
        'is_admin': is_admin,
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
            user.imatgePerfil = profile_image.name  # Store only the name of the image

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




from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Log
from .serializers import LogSerializer

from biblioteca.models import User  # Importa tu modelo de usuario personalizado

@api_view(['POST'])
def create_log(request):
    logs = request.data
    responses = []
    for log in logs:
        try:
            # Buscar el usuario por su nombre de usuario
            log['usuari'] = User.objects.get(username=log['usuari'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

        serializer = LogSerializer(data=log)
        if serializer.is_valid():
            serializer.save()
            responses.append(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    return Response(responses, status=201)