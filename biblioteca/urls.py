from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/passwordreset.html",
        extra_context={'domain': settings.DOMAIN_NAME}
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/passwordresetdone.html"
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name='password_reset_complete'),
]