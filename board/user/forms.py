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
    bio = forms.CharField(max_length=200, label="Biografía", required=False, widget=forms.Textarea)
    phone = forms.CharField(label='Teléfono*', validators=[RegexValidator(r'^[0-9].{8,}$', 'El número de teléfono deben ser entre 9 y 10 dígitos')], max_length=10, required=True,
    widget= forms.TextInput(attrs={'size': '25'}))
    address = forms.CharField(max_length=150, label="Dirección*", required=True,widget= forms.TextInput(attrs={'size': '25'}))
    check_terms = forms.BooleanField(label="Acepto Términos y Condiciones de uso*", required=True)
    check_privacy = forms.BooleanField(label="Acepto la política de privacidad*", required=True)
    
class editAccount(forms.Form):
    username = forms.CharField(max_length=20,label="Usuario")
    password3 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Contraseña actual*")
    password1 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Nueva contraseña*")
    password2 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Repetir nueva contraseña*")

class editProfile(forms.Form):
    name = forms.CharField(max_length=40, label="Nombre")
    last_name = forms.CharField(max_length=50, label="Apellidos")
    email = forms.CharField(max_length=50, label="Email", validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200, label="Biografía", required=False, widget=forms.Textarea)
    phone = forms.CharField(label='Teléfono*', validators=[RegexValidator(r'^[0-9].{8,}$', 'El numero de telefono deben ser entre 9 y 10 digitos')], max_length=10, required=True, widget=forms.TextInput(attrs={'size': '25'}))
    address = forms.CharField(max_length=150, label="Dirección", required=True)


class editPic(forms.Form):
    picture = forms.FileField(label="Foto",required=False)


class contact(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


class descargaDatos(forms.Form):
    message = forms.CharField(min_length=0 ,max_length=200,label="Mensaje",required=False,widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Contraseña', strip=False, widget=forms.PasswordInput)
