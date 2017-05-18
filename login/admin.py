from django.contrib import admin
from django.contrib.auth.models import Group

nombres_grupo= ["Administrador","Clientes"]

for group in nombres_grupo :
    if (Group.objects.filter(name=group).count()==0) :
        grupo= Group.objects.create(name=group)
