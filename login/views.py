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
import time
import hashlib
import random


def validate_username(request):
    username = request.POST.get('username', None)
    data = {
        'username_exists': User.objects.filter(username=username).exists()
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
    data = {
        'email_exists': User.objects.filter(email=email).exists()
    }

    if not data['email_exists']:
        data['error'] = 'El email ingresado no existe, por favor intente nuevamente'

    return JsonResponse(data)


def groups():
    nombres_grupo = ["Administrador", "Clientes"]

    for group in nombres_grupo:
        if Group.objects.filter(name=group).count() == 0:
            Group.objects.create(name=group)


def get_user(user):
    if user.is_staff:
        return 'welcomeStaff'
    else:
        return 'welcome'


def create_token():
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz0123456789')
    random.shuffle(chars)
    chars = ''.join(chars)
    sha1 = hashlib.sha1(chars.encode('utf8'))
    token = sha1.hexdigest()
    key = token[:15]
    return key


def authenticate_user(username=None):
    """ Authenticate a user based on email address as the user name. """
    try:
        user = User.objects.get(email=username)
        if user is not None:
            return user, 1
    except User.DoesNotExist:
        try:
            user = User.objects.get(username=username)
            if user is not None:
                return user, 2
        except User.DoesNotExist:
            return None, 0


def send_email(subject, message_template, context, email):
    from_email = 'Aplicacion Prueba'
    email_subject = subject
    message = get_template(message_template).render(context)
    msg = EmailMessage(email_subject, message, to=[email], from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    print("Se envió exitosamente el correo.")


def email_login_successful(user):
    usuario = user.get_full_name()
    formato = "%d-%m-%y %I:%m:%S %p"
    date_time = user.last_login.strftime(formato).split(" ")
    date = date_time[0]
    time = date_time[1] + " " + date_time[2]

    c = {'usuario': usuario,
         'fecha': date,
         'hora': time}

    subject = 'Aplicación Prueba - Bienvenido a Nuestra Aplicación'
    message_template = 'email_login.html'
    send_email(subject, message_template, c, user.email)


def new_Token(request, pk):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('logout'))

    user = User.objects.get(pk=pk)
    UserProfile.objects.filter(user=user).delete()
    key = create_token()
    while UserProfile.objects.filter(activation_key=key).count() > 0:
        key = create_token()
    key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
    new_profile = UserProfile(user=user, activation_key=key,
                              key_expires=key_expires)
    try:
        c = {'usuario': user.get_full_name,
             'key': key,
             'host': request.META['HTTP_HOST']}
        subject = 'Aplicación Prueba - Código Activación de cuenta'
        message_template = 'success.html'
        email = user.email
        send_email(subject, message_template, c, email)
    except:
        render(request, 'success.html', c)
    new_profile.save()
    return render(request, 'success.html', c)


def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('logout'))

    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    user = user_profile.user

    time = datetime.datetime.today()

    if user_profile.key_expires < time:
        return HttpResponseRedirect(reverse_lazy('new_Token',
                                                 kwargs={'pk': user.pk}))

    c = {'usuario': user.get_full_name,
         'host': request.META['HTTP_HOST']}

    if request.method == 'GET':
        user.is_active = True
        user.save()
        try:
            subject = 'Aplicación Prueba - Cuenta Activada'
            message_template = 'account_active.html'
            email = user.email
            send_email(subject, message_template, c, email)
        except:
            pass

    return render(request, 'account_active.html', c)


def pass_restore(request, token, id):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('logout'))

    user_profile = get_object_or_404(UserProfile, activation_key=token, user=id)
    user = user_profile.user

    time = datetime.datetime.today()

    if user_profile.key_expires < time:
        form = forgotUser_PassForm()
        msg = "Su link caducó. Por favor solicite de nuevo el cambio de contraseña."
        form.add_error(None, msg)
        return render(request, 'forgotUser_Pass.html', {'form': form})

    c = {'usuario': user.get_full_name,
         'host': request.META['HTTP_HOST']}

    if request.method == 'GET':
        user.is_active = True
        user.save()
        try:
            subject = 'Aplicación Prueba - Cuenta Activada'
            message_template = 'account_active.html'
            email = user.email
            send_email(subject, message_template, c, email)
        except:
            pass

    return render(request, 'account_active.html', c)


def user_block(user):
    try:
        user.is_active = False
        user.save()
        c = {'usuario': user.get_full_name}
        subject = 'Aplicación Prueba - Cuenta Desactivada '
        message_template = 'account_block.html'
        email = user.email
        send_email(subject, message_template, c, email)
    except:
        pass


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('logout'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth, choices = authenticate_user(username)
            msg_error = " Recuerde: Al realizar tres intentos erróneos su cuenta será bloqueada."
            error_username = "Tu username  o contraseña no son correctos." + msg_error
            error_email = "Tu correo o contraseña no son correctos." + msg_error
            if user_auth is not None:
                users = User.objects.get(username=username)
                user_profile = get_object_or_404(UserProfile, user=users)
                if user_auth.is_active and user_profile.intent < 3:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    if user:
                        login(request, user)
                        try:
                            email_login_successful(user)
                        except:
                            pass
                        user_profile.intent = 0
                        user_profile.save()
                        template = get_user(users)
                        return HttpResponseRedirect(reverse_lazy(template))
                    else:
                        if choices == 1:
                            form.add_error(None, error_email)
                        else:
                            form.add_error(None, error_username)

                        today = datetime.datetime.today().date()

                        if user_profile.date_intent != today:
                            user_profile.intent = 1
                            user_profile.date_intent = today
                        else:
                            user_profile.intent = user_profile.intent + 1

                        user_profile.save()
                elif user_profile.intent == 3:
                    msg = "Su cuenta ha sido bloqueada. Comuniquese con el administrador" \
                          " para iniciar el proceso de desbloqueo."
                    print(msg)
                    form.add_error(None, msg)
                    user_block(users)
                else:
                    msg = "Aún no has confirmado tu cuenta. Por favor revise su correo."
                    form.add_error(None, msg)
                    user = None
            else:
                if choices == 1:
                    form.add_error(None, error_email)
                else:
                    form.add_error(None, error_username)
        else:
            context = {'form': form}
            return render(request, 'login.html', context)
    else:
        form = LoginForm()
    context = {'form': form, 'host': request.get_host()}
    return render(request, 'login.html', context)


def LoginEmail(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('logout'))

    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_auth, choices = authenticate_user(username)
            if choices == 1:
                if user_auth is not None:
                    if user_auth.is_active:
                        user = authenticate(username=user_auth.username,
                                            password=password)

                        if user:
                            login(request, user)
                            get_user(user)
                        else:
                            form.add_error(
                                None, "Tu correo o contraseña no son correctos")

                    else:
                        form.add_error(None, "Aún no has confirmado tu correo.")
                        user = None
                else:
                    form.add_error(None, "Tu correo o contraseña no son correctos")
            else:
                form.add_error(None, "Debe ingresar un correo válido")
        else:
            context = {'form': form}
            return render(request, 'loginEmail.html', context)
    else:
        form = EmailForm()
    context = {'form': form, 'host': request.get_host()}
    return render(request, 'loginEmail.html', context)


def user_loginUsername(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('logout'))

    if request.method == 'POST':
        form = Login_UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth, choices = authenticate_user(username)
            if choices == 2:
                if user_auth is not None:
                    if user_auth.is_active:
                        user = authenticate(username=user_auth.username,
                                            password=password)

                        if user:
                            login(request, user)
                            get_user(user)
                        else:
                            form.add_error(
                                None, "Tu username o contraseña no son correctos")

                    else:
                        form.add_error(None, "Aún no has confirmado tu correo.")
                        user = None
                else:
                    form.add_error(None, "Tu username o contraseña no son correctos")
            else:
                form.add_error(None, "Debe ingresar un username válido")

        else:
            context = {'form': form}
            return render(request, 'loginUsername.html', context)
    else:
        form = Login_UsernameForm()
    context = {'form': form, 'host': request.get_host()}
    return render(request, 'loginUsername.html', context)


class Home(TemplateView):
    template_name = 'base.html'


class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

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
            first_name = post_values['first_name']
            last_name = post_values['last_name']
            email = post_values['email']
            username = post_values['username']
            password = post_values['password']
            user = User(first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password)
            user.set_password(password)
            user.is_active = False
            group = Group.objects.get(name="Clientes")

            try:
                activation_key = create_token()
                while UserProfile.objects.filter(activation_key=activation_key).count() > 0:
                    activation_key = create_token()
                c = {'usuario': user.get_full_name,
                     'key': activation_key,
                     'host': request.META['HTTP_HOST']}
                subject = 'Aplicación Prueba - Activación de cuenta'
                message_template = 'success.html'
                email = user.email
                send_email(subject, message_template, c, email)
            except:
                form.add_error(
                    None, "Hubo un error en la conexión intente registrarse de nuevo. Gracias")
                context = {'form': form, 'host': request.get_host()}
                return render(request, 'register.html', context)

            user.save()
            user.groups.add(group)
            key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
            user_profile = UserProfile(user=user, activation_key=activation_key,
                                       key_expires=key_expires)
            user_profile.save()
            return render(request, 'success.html', c)
        else:
            return render(request, 'register.html', {'form': form})


class Success(TemplateView):
    template_name = 'success.html'


class Welcome(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'


class WelcomeStaff(LoginRequiredMixin, TemplateView):
    template_name = 'welcomeStaff.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'


class Active(TemplateView):
    template_name = 'account_active.html'


class Block(TemplateView):
    template_name = 'account_block.html'


class ForgotUsername(FormView):
    template_name = 'forgotUser_Pass.html'
    form_class = forgotUser_PassForm

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        post_values = request.POST.copy()
        form = forgotUser_PassForm(post_values)
        if form.is_valid():
            # Guardamos los datos

            return render(request, 'success.html')
        else:
            return render(request, 'forgotUser_Pass.html', {'form': form})


class ForgotPassword(FormView):
    template_name = 'forgotUser_Pass.html'
    form_class = forgotUser_PassForm

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        post_values = request.POST.copy()
        print(request.POST)
        form = forgotUser_PassForm(post_values)
        if form.is_valid():
            email = post_values['email']
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    try:
                        activation_key = create_token()
                        while UserProfile.objects.filter(activation_key=activation_key).count() > 0:
                            activation_key = create_token()

                        c = {'usuario': user.get_full_name,
                             'id': user.id,
                             'key': activation_key,
                             'host': request.META['HTTP_HOST']}
                        subject = 'Aplicación Prueba - Solicitud de cambio de contraseña'
                        message_template = 'pass_restore_email.html'
                        send_email(subject, message_template, c, email)
                    except:
                        form.add_error(
                            None, "Hubo un error en la conexión intente de nuevo. Gracias")
                        context = {'form': form, 'host': request.get_host()}
                        return render(request, 'forgotUser_Pass.html', context)
                else:
                    msg = "Aún no has confirmado tu cuenta. Por favor revise su correo."
                    form.add_error(None, msg)
                    return render(request, 'login.html', {'form': form})
            except User.DoesNotExist:
                time.sleep(3)
                form = forgotUser_PassForm()
                return render(request, 'forgotUser_Pass.html', {'form': form})

            user_profile = UserProfile.objects.get(user=user)
            key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
            user_profile.key_expires = key_expires
            user_profile.activation_key = activation_key
            user_profile.save()

            form.add_error(None,"Ha solicitado cambiar su contraseña. Revise su correo.")
            context = {'form': form,
                       'usuario': user.get_full_name(),
                       'host': request.META['HTTP_HOST']}
            return render(request, 'restoreSuccess.html', context)
        else:
            pass