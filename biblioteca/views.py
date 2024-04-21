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

from .backends import EmailBackend
import os
from django.conf import settings

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
            return JsonResponse({'redirect': '/dashboard/'})  # Return a JSON response with the URL to redirect to
        else:
            # handle failed login case
            response = JsonResponse({'error': 'Invalid login credentials'})
            response.status_code = 401  # Or another appropriate HTTP status code
            return response
    else:
        return render(request, 'index.html')

# VIEW PARA REDIRIGIR AL USUARIO AL DASHBOARD CON EL TOKEN CSRF
from django.contrib.auth import get_user_model

@login_required
def dashboard_view(request):
    email = request.session.get('username')  # Assuming the email is stored in 'username'
    token = request.session.get('token')
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        is_admin = user.is_superuser or user.esAdmin
        username = user.username  # Fetch the username from the User model
    except User.DoesNotExist:
        is_admin = False
        username = None  # Set username to None if the user does not exist
    return render(request, 'dashboard.html', {'username': username, 'token': token, 'is_admin': is_admin})

# VIEW PARA EL PERFIL DEL USUARIO
@login_required
def profile(request):
    # Obtén el usuario actual
    user = request.user

    # Puedes acceder a los atributos del usuario, como username y email
    username = user.username
    email = user.email
    dataNaixement = user.dataNaixement
    cicle = user.cicle

    # También puedes verificar si el usuario es un administrador
    is_admin = user.is_superuser

    # Pasa estos datos al contexto del template
    context = {
        'username': username,
        'email': email,
        'is_admin': is_admin,
        'dataNaixement': dataNaixement,
        'cicle': cicle,
    }

    # Renderiza el template con este contexto
    return render(request, 'perfil.html', context)



@login_required
def edit_profile(request):
    user = request.user
    username = user.username

    is_admin = user.is_superuser


    context = {
        'username': username,
        'email': user.email,
        'is_admin': is_admin,
        'dataNaixement': user.dataNaixement,  # Assuming the User model has a dataNaixement field
        'cicle': user.cicle,  # Assuming the User model has a cicle field
    }
    return render(request, 'editarPerfil.html', context)



@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.dataNaixement = request.POST['dataNaixement']  # Assuming the User model has a dataNaixement field
        user.cicle = request.POST['cicle']  # Assuming the User model has a cicle field
        user.save()
        #messages.success(request, 'Your profile was successfully updated!')
        return redirect('edit_profile')
    else:
        return redirect('edit_profile')