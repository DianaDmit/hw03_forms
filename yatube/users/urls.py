from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Форма регистрации на сайте
    path(
        'signup/',
        views.SignUp.as_view(template_name='users/signup.html'),
        name='signup'
    ),
    # Форма после выхода из учетной записи
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    # Форма входа на сайт
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    # Форма сброса пароля
    path(
        'password_reset/',
        PasswordResetView.as_view
        (template_name='users/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view
        (template_name='users/password_change.html'),
        name='password_change',
    ),

    path(
        'password_change/done/', PasswordChangeDoneView.as_view
        (template_name='users/password_change_done.html'),
    ),

    path(
        'password_reset/done/', PasswordResetDoneView.as_view
        (template_name='users/password_reset_done.html'),
    ),

    path(
        'reset/<uidb64>/<token>/', PasswordChangeView.as_view
        (template_name='users/password_reset_confirm.html'),
    ),

    path(
        'reset/done/', PasswordResetCompleteView.as_view
        (template_name='users/password_reset_complete.html'),
    ),
]
