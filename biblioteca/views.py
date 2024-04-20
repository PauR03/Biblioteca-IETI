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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from biblioteca.models import User

@login_required
def dashboard_view(request):
    email = request.session.get('username')  # Assuming the email is stored in 'username'
    token = request.session.get('token')
    try:
        user = User.objects.get(email=email)
        is_admin = user.is_superuser or user.esAdmin
    except User.DoesNotExist:
        is_admin = False
    return render(request, 'dashboard.html', {'username': email, 'token': token, 'is_admin': is_admin})