from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .backends import EmailBackend
from django.http import JsonResponse
from django.contrib.auth.models import User
import os
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required


from django.shortcuts import redirect

from django.shortcuts import redirect

from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        backend = EmailBackend()
        user = backend.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.session['username'] = username
            request.session['token'] = token.key
            return redirect('dashboard')  # Redirect to the 'dashboard' view
        else:
            # manejar el caso de inicio de sesión fallido
            response = HttpResponse('Invalid login credentials')
            response.status_code = 401  # Or another appropriate HTTP status code
            return response
    else:
        return render(request, 'index.html')

@login_required
def dashboard_view(request):
    username = request.session.get('username')
    token = request.session.get('token')
    return render(request, 'dashboard.html', {'username': username, 'token': token})

