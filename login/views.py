from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth import *
from django.contrib import messages
from login.forms import *


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
            user= form.save()
            user.first_name = post_values['first_name']
            user.last_name = post_values['last_name']
            user.email = post_values['email']
            user.username = post_values['username']
            user.password = post_values['password']
            user.save()
            return HttpResponseRedirect(reverse_lazy('success_register'))
        else:
            return render(request,'register.html',{'form': form})


class Login (FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user_auth = authenticate(username=username, password=password)
            if user_auth is not None:
                if user_auth.is_active:
                    login(request, user_auth)
                    return HttpResponseRedirect(reverse_lazy('welcome'))
                else:
                    messages.error(request, "Aún no has confirmado tu correo.")
                    return render(request, 'login.html',
                                  {'form': form})
            else:
                messages.error(request, "Lo sentimos, su correo o contraseña no son correctos.")
                return render(request, 'login.html',
                              {'form': form})
        else:
            return render(request, 'login.html', {'form': form})

class Success (TemplateView):
    template_name = 'success.html'

class Welcome (TemplateView):
    template_name = 'welcome.html'



