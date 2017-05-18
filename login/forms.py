#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):

    password2 = forms.CharField(
        label="Repita la Contraseña",
        widget=forms.PasswordInput()
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'username', 'password']

        labels = {
            'first_name': 'Nombre: ',
            'last_name': 'Apellido: ',
            'email': 'Correo: ',
            'username': 'Username: ',
        }




class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','password']

        labels = {
            'username': 'Username: ',
            'password': 'Contraseña: '
        }
