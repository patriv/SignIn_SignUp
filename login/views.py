#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from login.forms import *
from login.models import *
import datetime
import hashlib
import random


def validate_username(request):
    username = request.POST.get('username',None)
    data = {
        'username_exists':User.objects.filter(username=username).exists()
    }

    if data['username_exists']:
        data['error'] = 'El username escogido no está disponible.'

    return JsonResponse(data)


def validate_email(request):
    email = request.POST.get('email', None)
    data = {
        'email_exists': User.objects.filter(email=email).exists()
    }

    if data['email_exists']:
        data['error'] = 'El email ingresado ya está registrado, por favor intente nuevamente'

    return JsonResponse(data)


def forgot_email(request):
    email = request.POST.get('email', None)
    print(email)
    data = {
        'email_exists': User.objects.filter(email=email).exists()
    }

    if data['email_exists'] == False:
        print("en if")
        data['error'] = 'El email ingresado no existe, por favor intente nuevamente'

    return JsonResponse(data)


def groups():
        nombres_grupo= ["Administrador","Clientes"]

        for group in nombres_grupo :
            if (Group.objects.filter(name=group).count()==0) :
                grupo= Group.objects.create(name=group)


def create_token():
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz0123456789')
    random.shuffle(chars)
    chars = ''.join(chars)
    sha1 = hashlib.sha1(chars.encode('utf8'))
    token = sha1.hexdigest()
    key = token[:12]
    return key


def authenticate_user(username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user is not None:
                return user,1
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user is not None:
                    return user,2
            except User.DoesNotExist:
                return None,0


def email_login_successfull(user):
    usuario = user.get_full_name()
    date = user.last_login.date
    time = str(user.last_login.hour) + ":" + str(user.last_login.minute)
    time += ":" + str(user.last_login.second)

    c = {'usuario': usuario,
         'fecha': date,
         'hora':time}
    from_email = 'Aplicacion Prueba'
    email_subject = 'Aplicación Prueba - Bienvenido a Nuestra Aplicación'
    message = get_template('email_login.html').render(c)
    msg = EmailMessage(email_subject, message, to=[user.email], from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()


def new_Token(request, pk):
    if request.user.is_authenticated():
            HttpResponseRedirect(reverse_lazy('home'))

    user = User.objects.get(pk=pk)
    UserProfile.objects.filter(user=user).delete()
    key = create_token()
    key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
    new_profile = UserProfile(user=user, activation_key=key,
                              key_expires=key_expires)
    new_profile.save()
    c = {'usuario': user.get_full_name,
         'key': key,
         'host': request.META['HTTP_HOST']}
    from_email = 'Aplicacion Prueba'
    email_subject = 'Aplicación Prueba - Código Activación de cuenta'
    message = get_template('success.html').render(c)
    msg = EmailMessage(email_subject, message, to=[user.email], from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return render(request, 'success.html', c)


def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        HttpResponseRedirect(reverse_lazy('home'))

    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    user = user_profile.user

    time = datetime.datetime.today()

    if user_profile.key_expires < time:
        return HttpResponseRedirect(reverse_lazy('new_Token',
             kwargs={'pk': user.pk}))

    if request.method == 'GET':
        user.is_active = True
        user.save()
        c = {'usuario': user.get_full_name,
            'host': request.META['HTTP_HOST']}
        from_email = 'Aplicacion Prueba'
        email_subject = 'Aplicación Prueba - Cuenta Activada'
        message = get_template('account_active.html').render(c)
        msg = EmailMessage(email_subject, message, to=[user.email], from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    return render(request, 'account_active.html', c)


class Active(TemplateView):
    template_name = 'account_active.html'


def user_login(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect(reverse_lazy('welcomeStaff'))
        else:
            return HttpResponseRedirect(reverse_lazy('welcome'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth, choices = authenticate_user(username, password)
            if user_auth is not None:
                if user_auth.is_active:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    if user:
                        login(request, user)
                        email_login_successfull(user)
                        if user.is_staff or user.is_superuser:
                            return HttpResponseRedirect(reverse_lazy('welcomeStaff'))
                        else:
                            return HttpResponseRedirect(reverse_lazy('welcome'))
                    else:
                        if (choices == 1) :
                            form.add_error(
                                None, "Tu correo o contraseña no son correctos")
                        else :
                            form.add_error(
                                None, "Tu username o contraseña no son correctos")
                else:
                    form.add_error(None, "Aún no has confirmado tu correo.")
                    user = None
            else:
                if (choices == 1) :
                            form.add_error(
                                None, "Tu correo o contraseña no son correctos")
                else :
                    form.add_error(
                        None, "Tu username o contraseña no son correctos")
        else:
            context = {'form': form}
            return render(request, 'login.html',context)
    else:
        form = LoginForm()
    context = {'form': form, 'host': request.get_host()}
    return render(request,'login.html', context)


def user_loginEmail(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('welcome'))
    
    if request.method == 'POST':
        form = Login_EmailForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth, choices = authenticate_user(username, password)
            if user_auth is not None:
                if user_auth.is_active:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(reverse_lazy('welcome'))
                    else:
                        if (choices == 1) :
                            form.add_error(
                                None, "Tu correo o contraseña no son correctos")
                        else :
                            form.add_error(
                                None, "Tu username o contraseña no son correctos")
                else:
                    form.add_error(None, "Aún no has confirmado tu correo.")
                    user = None
            else:
                if (choices == 1) :
                            form.add_error(
                                None, "Tu correo o contraseña no son correctos")
                else :
                    form.add_error(
                        None, "Tu username o contraseña no son correctos")
        else:
            context = {'form': form}
            return render(request, 'loginEmail.html',context)
    else:
        form = LoginForm()
    context = {'form': form, 'host': request.get_host()}
    return render(request,'loginEmail.html', context)


def user_loginUsername(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('welcome'))
    
    if request.method == 'POST':
        form = Login_UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth, choices = authenticate_user(username, password)
            if user_auth is not None:
                if user_auth.is_active:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(reverse_lazy('welcome'))
                    else:
                        if (choices == 1) :
                            form.add_error(
                                None, "Tu correo o contraseña no son correctos")
                        else :
                            form.add_error(
                                None, "Tu username o contraseña no son correctos")
                else:
                    form.add_error(None, "Aún no has confirmado tu correo.")
                    user = None
            else:
                if (choices == 1) :
                            form.add_error(
                                None, "Tu correo o contraseña no son correctos")
                else :
                    form.add_error(
                        None, "Tu username o contraseña no son correctos")
        else:
            context = {'form': form}
            return render(request, 'loginUsername.html',context)
    else:
        form = LoginForm()
    context = {'form': form, 'host': request.get_host()}
    return render(request,'loginUsername.html', context)    


class Home (TemplateView):
    template_name = 'base.html'


class Registro (FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super(
            Registro, self).get_context_data(**kwargs)
        return context


    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        post_values = request.POST.copy()
        form = RegisterForm(post_values)
        if form.is_valid():
            # Guardamos los datos
            groups()

            user= form.save()
            user.first_name = post_values['first_name']
            user.last_name = post_values['last_name']
            user.email = post_values['email']
            user.username = post_values['username']
            password = post_values['password']
            user.set_password(password)
            user.is_active = False;
            user.save()

            group = Group.objects.get(name="Clientes")
            user.groups.add(group)

            activation_key = create_token()
            key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
            user_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            user_profile.save()

            c = {'usuario': user.get_full_name,
                 'key': activation_key,
                 'host': request.META['HTTP_HOST']}
            from_email = 'Aplicacion Prueba'
            email_subject = 'Aplicación Prueba - Activación de cuenta'
            message = get_template('success.html').render(c)
            msg = EmailMessage(email_subject, message, to=[user.email], from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

            return render(request, 'success.html', c)
        else:
            return render(request,'register.html',{'form': form})


class Success (TemplateView):
    template_name = 'success.html'


class Welcome (LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'


class WelcomeStaff(LoginRequiredMixin, TemplateView):
    template_name = 'welcomeStaff.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'


class ForgotUsername (FormView):
    template_name = 'forgotUsername.html'
    form_class = forgotUsernameForm

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        post_values = request.POST.copy()
        form = forgotUsernameForm(post_values)
        if form.is_valid():
            # Guardamos los datos

            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return render(request,'forgotUsername.html',{'form': form})


class ForgotPassword(FormView):
    template_name = 'forgotUsername.html'
    form_class = forgotUsernameForm

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        post_values = request.POST.copy()
        form = forgotUsernameForm(post_values)
        if form.is_valid():
            # Guardamos los datos

            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return render(request,'forgotUsername.html',{'form': form})


