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
    path('usuaris/', usuaris_view, name='usuaris'),
    path('perfil/', profile, name='profile'),
    path('editar_perfil/', edit_profile, name='editar_perfil'),
    path('update_profile/', update_profile, name='update_profile'),  # VIEW QUE INSERTA LOS DATOS MODIFICADOS DEL USAURIO EN LA BASE DE DATOS
    path('get_profile_image/', get_profile_image, name='get_profile_image'),
    path('autocomplete/', AutocompleteView.as_view(), name='autocomplete'),
    path('detall_cataleg/', product_detail, name='detall_cataleg'),
    path('editar_perfil/<int:id>', edit_profile_user, name='edit_profile_user'),
    path('update_profile_user/<int:id>', update_profile_user, name='update_profile_user'),
    path('prestecs/', prestecs, name='prestecs'),

    path('accounts/login/', login_view, name='login'),  
    path('api/create_log/', create_log, name='create_log'),
    path('api/getUsers/', getUsers, name='getUsers'),
    path('crearUsuario/', crear_usuario, name='crear_usuario'),
    path('importar_usuarios/', importar_usuarios, name='importar_usuarios'),

    path('api/getPrestecs/', getPrestecs, name='getPrestecs'),
    path('api/updatePrestec/', updatePrestec, name='updatePrestec'),
    path('api/autocompletePrestecs/', autocompletePrestecs, name='autocompletePrestecs'),
    path('api/autocompleteUsuaris/', autocompleteUsuaris, name='autocompleteUsuaris'),
    path('api/createPrestec/', createPrestec, name='createPrestec'),

    
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include('biblioteca.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)