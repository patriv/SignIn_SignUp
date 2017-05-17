from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'username', 'password']

        labels = {
            'first_name': 'Nombre: ',
            'last_name': 'Apellido: ',
            'email': 'Correo: ',
            'username': 'Username: ',
            'password': 'Contraseña: ',
            'password1': 'Repita la Contraseña: '
        }


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','password']

        labels = {
            'username': 'Username: ',
            'password': 'Contraseña: '
        }