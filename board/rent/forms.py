from .models import Game, Status
from django import forms
from django.core.validators import RegexValidator


name_regex = RegexValidator(regex=r'[^-><=.,^*/()%$·#!¡¿?|ºª´¨;:]', message="El nombre debe contener números, carácteres del alfabeto y/o espacios")

my_default_errors = {
    'invalid_image':'Selecciona una imagen correcta. El fichero seleccionado no pertenece a un formato correcto o está corrupto.'
}

class NewGame(forms.Form):
   name = forms.CharField(max_length=20,label="Nombre", validators=[name_regex])
   description = forms.CharField(max_length=200,label="Descripción",widget=forms.Textarea)
   price = forms.CharField(max_length=5,label="Precio (€/día)*", required=False)
   status = forms.ChoiceField(choices=[(str(x),x.value) for x in Status], label="Estado")
   picture = forms.ImageField( label="Foto",error_messages=my_default_errors)

class editData(forms.Form):
   name = forms.CharField(max_length=20,label="Nombre*", validators=[name_regex])
   description = forms.CharField(max_length=200,label="Descripción*",widget=forms.Textarea)
   price = forms.CharField(max_length=5,label="Precio (€/día)*",required=False)
   status = forms.ChoiceField(choices=[(str(x),x.value) for x in Status], label="Estado*")

class editPicture(forms.Form):
   picture = forms.ImageField( label="Foto*",error_messages=my_default_errors)
