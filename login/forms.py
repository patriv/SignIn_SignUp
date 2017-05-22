#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):

    password2 = forms.CharField(
        label="Repita la Contraseña: ",
        widget=forms.PasswordInput()
    )

    password = forms.CharField(
        label="Contraseña: ",
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

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        ##placeholder
        self.fields['first_name'].widget.attrs['placeholder'] = 'Sólo se admiten letras'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sólo se admiten letras'
        self.fields['password'].widget.attrs['placeholder'] = 'Sólo caracteres alfanuméricos'
        self.fields['password2'].widget.attrs['placeholder'] = 'Sólo caracteres alfanuméricos'
        self.fields['username'].widget.attrs['placeholder'] = 'Sólo caracteres alfanuméricos'
        self.fields['email'].widget.attrs['placeholder'] = 'Ej: nombre@example.com'


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=60, label=' Username o Email: ',
        required=True, widget=forms.TextInput(attrs={
            'class':"form-control",
            'id': "id_username",
            'placeholder' : ""
        }))
    password = forms.CharField(
        label="Contraseña: ", required=True, widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'type' :"Password",
            'id' : "id_password"
        }))

class Login_EmailForm(forms.Form):
    email = forms.CharField(
        max_length=60, label='Email: ',
        required=True, widget=forms.TextInput(attrs={
            'class':"form-control",
            'id': "id_email",
            'placeholder' : "ej: nombre@ejemplo.com"
        }))
    password = forms.CharField(
        label="Contraseña: ", required=True, widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'type' :"Password",
            'id' : "id_password"
        }))

class Login_UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=60, label='Username: ',
        required=True, widget=forms.TextInput(attrs={
            'class':"form-control",
            'id': "id_username",
            'placeholder' : "Sólo caracteres alfanumérico"
        }))
    password = forms.CharField(
        label="Contraseña: ", required=True, widget=forms.TextInput(attrs={
            'class' : "form-control",
            'type' :"Password",
            'id' : "id_password"
        }))


class forgotUsernameForm(forms.Form):
    email = forms.CharField(
        label = 'Email: ',
        required= True,
        widget= forms.EmailInput()
    )
