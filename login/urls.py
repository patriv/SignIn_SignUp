from django.conf.urls import url
import django.contrib.auth.views
from login.views import *

urlpatterns = [
    url(
        r'^$',
        Home.as_view(),
        name='home'),
    url(
        r'^login',
        user_login,
        name='login'),
    url(
        r'^emailLogin',
        user_loginEmail,
        name='EmailLogin'),

    url(
        r'^usernameLogin',
        user_loginUsername,
        name='UsernameLogin'),

    url(
        r'^logout',
        django.contrib.auth.views.logout,
        {
            'next_page': 'home'
        },
        name='logout'),
    url(
        r'^register',
        Registro.as_view(),
        name='registro'),
    url(
        r'^activate/(?P<activation_key>\w+)/$',
        register_confirm,
        name='register_confirm'),
    url(
        r'^sucessRegister',
        Success.as_view(),
        name='success_register'),
    url(
        r'^welcome',
        Welcome.as_view(),
        name='welcome'),
    url(
        r'^ajax/validate_username/$',
        validate_username,
        name='validate_username'),

    url(
        r'^ajax/validate_email/$',
        validate_email,
        name='validate_email'),

    url(
        r'^ajax/forgot_email/$',
        forgot_email,
        name='ajax_forgot_email'),

    url(
        r'^forgotUsername/$',
        ForgotUsername.as_view(),
        name='forgot_username'),


]