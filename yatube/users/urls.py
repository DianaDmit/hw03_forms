from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Форма регистрации на сайте
    path('signup/', views.SignUp.as_view(template_name='users/signup.html'), name='signup'),
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
        PasswordResetView.as_view(template_name='users/'
                                                'password_reset_form.html'),
        name='password_reset_form'
    ),
]
