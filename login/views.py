#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from login.forms import *
from django.http import JsonResponse
from django.contrib.auth.models import User, Group


def validate_username(request):
    username = request.POST.get('username',None)
    data = {
        'username_exists':User.objects.filter(username=username).exists()
    }
    
    if data['username_exists']:
        data['error'] = 'El username escogido no está disponible.'

    return JsonResponse(data)


def groups():
        nombres_grupo= ["Administrador","Clientes"]

        for group in nombres_grupo :
            if (Group.objects.filter(name=group).count()==0) :
                grupo= Group.objects.create(name=group)


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


def user_login(request):
    if request.user.is_authenticated():
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
            user.save()
            group = Group.objects.get(name="Clientes")
            user.groups.add(group)
            return HttpResponseRedirect(reverse_lazy('success_register'))
        else:
            return render(request,'register.html',{'form': form})


class Success (TemplateView):
    template_name = 'success.html'


class Welcome (LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'
