from django.conf.urls import url
from login.views import *

urlpatterns = {
    url(
        r'^$',
        Home.as_view(),
        name='home'),
    url(
        r'^register',
        Registro.as_view(),
        name='registro'),
    url(
        r'^login',
        Login.as_view(),
        name='login'),
    url(
        r'^sucessRegister',
        Success.as_view(),
        name='success_register'),
    url(
        r'^welcome',
        Welcome.as_view(),
        name='welcome'),
}