from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .backends import EmailBackend

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        backend = EmailBackend()
        user = backend.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'dashboard.html', {'username': username})  
        else:
            # manejar el caso de inicio de sesión fallido
            return render(request, 'index.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'index.html')
    
