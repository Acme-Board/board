from django import forms

from .models import User
from django import forms
from django.core.validators import EmailValidator, URLValidator



class Register(forms.Form):
    username = forms.CharField(max_length=20,label="Usuario")
    password1 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(max_length=32,widget=forms.PasswordInput,label="Repetir contraseña")
    name = forms.CharField(max_length=40,label="Nombre")
    last_name = forms.CharField(max_length=50,label="Apellidos")
    email = forms.CharField(max_length=50,label="email",validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200,label="Descripción",required=False,widget=forms.Textarea)
    picture =  forms.FileField(label="Foto")
    