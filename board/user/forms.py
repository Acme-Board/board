from django import forms

from .models import User
from django import forms
from django.core.validators import EmailValidator, URLValidator, RegexValidator, validate_image_file_extension

#Forms here

phone_regex = RegexValidator(regex=r'^[0-9]{9}$', message="El número de teléfono es incorrecto. Deben ser 9 números consecutivos. Ej: 966966966")
name_regex = RegexValidator(regex=r'^[a-zA-Z ]\S+\s*', message="El nombre debe contener carácteres del alfabeto y/o espacios")
last_name_regex = RegexValidator(regex=r'^[a-zA-Z ]\S+\s*', message="Los apellidos deben contener carácteres del alfabeto y/o espacios")
username_regex = RegexValidator(regex=r'.*([a-zA-Z]{1,}).*([a-zA-Z]{1,}).*([a-zA-Z]{1,}).*', message="El nombre de usuario debe contener al menos 3 letras")

my_default_errors = {
    'invalid_image':'Selecciona una imagen correcta. El fichero seleccionado no pertenece a un formato correcto o está corrupto.'
}

class Register(forms.Form):
    username = forms.CharField(max_length=20, label="Usuario*", validators=[username_regex], widget= forms.TextInput(attrs={'size': '25'}))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'size': '25'}), label="Contraseña*")
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'size': '25'}), label="Repetir contraseña*")
    name = forms.CharField(max_length=40, label="Nombre*", validators=[name_regex], widget= forms.TextInput
                           (attrs={'size': '25'}))
    last_name = forms.CharField(max_length=50, label="Apellidos*", validators=[last_name_regex], widget= forms.TextInput
                           (attrs={'size': '25'}))
    email = forms.CharField(max_length=50, widget= forms.TextInput
                           (attrs={'size': '25','placeholder':'correo@servidor.com'}) ,label="Email*", validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200, label="Biografía", required=False, widget=forms.Textarea)
    phone = forms.CharField(label='Teléfono*', validators=[phone_regex], max_length=10, required=True,
                            widget= forms.TextInput(attrs={'size': '25','placeholder':'966966966'}))
    address = forms.CharField(max_length=150, label="Dirección*", required=True,widget= forms.TextInput(attrs={'size': '25'}))
    check_terms = forms.BooleanField(label="Acepto Términos y Condiciones de uso*", required=True)
    check_privacy = forms.BooleanField(label="Acepto la política de privacidad*", required=True)
    
class editPass(forms.Form):
    password3 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Contraseña actual*")
    password1 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Nueva contraseña*")
    password2 = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Repetir nueva contraseña*")

class editUsername(forms.Form):
    username = forms.CharField(max_length=20,label="Usuario*", validators=[username_regex])
    password = forms.CharField(max_length=32,widget=forms.PasswordInput, label="Contraseña actual*")

class editProfile(forms.Form):
    name = forms.CharField(max_length=40, validators=[name_regex], label="Nombre")
    last_name = forms.CharField(max_length=50, validators=[last_name_regex], label="Apellidos")
    email = forms.CharField(max_length=50, label="Email", validators=[EmailValidator(message="Email incorrecto")])
    bio = forms.CharField(max_length=200, label="Biografía", required=False, widget=forms.Textarea)
    phone = forms.CharField(label='Teléfono*', validators=[phone_regex], max_length=9, required=True, widget=forms.TextInput(attrs={'size': '25','placeholder':'666666666'}))
    address = forms.CharField(max_length=150, label="Dirección", required=True)


class editPic(forms.Form):
    picture = forms.ImageField(label="Foto",required=False,error_messages=my_default_errors)



class contact(forms.Form):
    message = forms.CharField(label="Mensaje",widget=forms.Textarea)


class descargaDatos(forms.Form):
    message = forms.CharField(min_length=0 ,max_length=200,label="Mensaje",required=False,widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Contraseña', strip=False, widget=forms.PasswordInput)
