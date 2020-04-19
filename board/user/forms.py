from django import forms

from .models import User
from django import forms
from django.core.validators import EmailValidator, URLValidator, RegexValidator

#Forms here

class Register(forms.Form):
    username = forms.CharField(max_length=20, label="Usuario*", widget= forms.TextInput(attrs={'size': '25'}))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'size': '25'}), label="Contraseña*")
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'size': '25'}), label="Repetir contraseña*")
    name = forms.CharField(max_length=40, label="Nombre*", widget= forms.TextInput
                           (attrs={'size': '25'}))
    last_name = forms.CharField(max_length=50, label="Apellidos*", widget= forms.TextInput
                           (attrs={'size': '25'}))
    email = forms.CharField(max_length=50, widget= forms.TextInput
                           (attrs={'size': '25','placeholder':'correo@servidor.com'}) ,label="Email*", validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200, label="Descripción", required=False, widget=forms.Textarea)
    phone = forms.CharField(label='Teléfono*', validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono inválido debe seguir el siguiente patrón +999 999999999')], max_length=17, required=True,
    widget= forms.TextInput(attrs={'size': '25'}))
    address = forms.CharField(max_length=150, label="Dirección*", required=True,widget= forms.TextInput(attrs={'size': '25'}))
    check = forms.BooleanField(label="Acepto Términos y Condiciones de uso*", required=True)

class editAccount(forms.Form):
    username = forms.CharField(max_length=20,label="Usuario")
    password3 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Contraseña actual*")
    password1 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Nueva contraseña*")
    password2 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Repetir nueva contraseña*")

class editProfile(forms.Form):
    name = forms.CharField(max_length=40, label="Nombre")
    last_name = forms.CharField(max_length=50, label="Apellidos")
    email = forms.CharField(max_length=50, label="Email", validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200, label="Descripción", required=False, widget=forms.Textarea)
    phone = forms.CharField(validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono inválido debe seguir el siguiente patrón +999 999999999')], max_length=17, required=True)
    address = forms.CharField(max_length=150, label="Dirección", required=True)


class editPic(forms.Form):
    picture = forms.FileField(label="Foto",required=False)


class contact(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


class descargaDatos(forms.Form):
    message = forms.CharField(max_length=200, label="Mensaje", required=False, widget=forms.Textarea)
