"""
URL configuration for bibliotecaIETI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from biblioteca.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_view, name='dashboard'),  
    path('perfil/', profile, name='profile'),
    path('editar_perfil/', edit_profile, name='editar_perfil'),
    path('perfil/', update_profile, name='update_profile'),  # VIEW QUE INSERTA LOS DATOS MODIFICADOS DEL USAURIO EN LA BASE DE DATOS
    path('get_profile_image/', get_profile_image, name='get_profile_image'),

    path('accounts/login/', login_view, name='login'),  

    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include('biblioteca.urls')),  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)