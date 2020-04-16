from django import forms

from .models import User
from django import forms
from django.core.validators import EmailValidator, URLValidator

#Forms here

class Register(forms.Form):
    username = forms.CharField(max_length=20,label="Usuario*")
    password1 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Contraseña*")
    password2 = forms.CharField(max_length=32,widget=forms.PasswordInput,label="Repetir contraseña*")
    name = forms.CharField(max_length=40,label="Nombre*")
    last_name = forms.CharField(max_length=50,label="Apellidos*")
    email = forms.CharField(max_length=50,label="Email*",validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200,label="Descripción",required=False,widget=forms.Textarea)
    check = forms.BooleanField(label="Acepto Términos y Condiciones de uso*", required=True)

class editAccount(forms.Form):
    username = forms.CharField(max_length=20,label="Nuevo usuario")
    password3 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Contraseña actual")
    password1 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Nueva contraseña")
    password2 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Repetir nueva contraseña")

class editProfile(forms.Form):
    name = forms.CharField(max_length=40,label="Nombre")
    last_name = forms.CharField(max_length=50,label="Apellidos")
    email = forms.CharField(max_length=50,label="email",validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200,label="Descripción",required=False,widget=forms.Textarea)

class editPic(forms.Form):
    picture = forms.FileField( label="Foto",required=False)

class contact(forms.Form):
    
    message = forms.CharField(widget=forms.Textarea)
class descargaDatos(forms.Form):
    
    message = forms.CharField(max_length=200,label="Message",required=False,widget=forms.Textarea)