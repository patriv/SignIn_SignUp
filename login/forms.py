#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length= 15, label = "Nombre: ",
        required = True, widget=forms.TextInput(attrs={
            'class': "form-control",
            'type': "text",
            'placeholder': "Sólo se admiten letras"
        })
    )

    last_name = forms.CharField(
        max_length=15, label= "Apellido",
        required=True, widget=forms.TextInput(attrs={
            'class': "form-control",
            'type': "text",
            'placeholder': "Sólo se admiten letras"
        })
    )

    email = forms.CharField(
        max_length= 60, label="email",
        required=True, widget=forms.EmailInput(attrs={
            'class': "form-control",
            'type' : 'email',
            'placeholder': "ej: nombre@ejemplo.com"
        })
    )

    username = forms.CharField(
        max_length=20, label = "Username",
        required=True, widget=forms.TextInput(attrs={
            'class': "form-control",
            'type': 'text',
            'placeholder': "Sólo caracteres alfanuméricos"
        })
    )
    password = forms.CharField(
        label="Contraseña: ",max_length=12,
        required= True, widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'type' :"Password",
            'id' : "id_password"
        })
    )

    password2 = forms.CharField(
        label="Repita la contraseña: ", max_length=12,
        required=True, widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'type' :"Password",
            'id' : "id_password2"
        })
    )

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'username', 'password']


class EmailForm(forms.Form):

    email = forms.CharField(
        max_length=60, label='Email: ',
        required=True, widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "id_email",
            'placeholder': "ej: nombre@ejemplo.com"
        }))

    password = forms.CharField(
        label="Contraseña: ", required=True, widget=forms.TextInput(attrs={
            'class' : "form-control",
            'type' :"Password",
            'id' : "id_password"
        })
    )


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=60, label=' Username o Email: ',
        required=True, widget=forms.TextInput(attrs={
            'class':"form-control",
            'id': "id_username",
            'placeholder': ""
        }))

    password = forms.CharField(
        label="Contraseña: ", required=True, widget=forms.PasswordInput(attrs={
            'class' : "form-control",
            'type' :"Password",
            'id' : "id_password"
        })
    )


class Login_UsernameForm(forms.Form):

    username = forms.CharField(
        max_length=60, label='Username: ',
        required=True, widget=forms.TextInput(attrs={
            'class':"form-control",
            'id': "id_username",
            'placeholder' : "Sólo caracteres alfanumérico"
        })
    )

    password = forms.CharField(
        label="Contraseña: ", required=True, widget=forms.TextInput(attrs={
            'class': "form-control",
            'type': "Password",
            'id': "id_password"
        })
    )


class forgotUser_PassForm(forms.Form):

    email = forms.CharField(
        label='Email: ',
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "id_email"
        })
    )
