from .models import Game, Status
from django import forms

class NewGame(forms.Form):
   name = forms.CharField(max_length=20,label="Nombre*")
   description = forms.CharField(max_length=200,label="Descripción*",widget=forms.Textarea)
   price = forms.CharField(max_length=5,label="Precio (€/día)*")
   status = forms.ChoiceField(choices=[(str(x),x.value) for x in Status], label="Estado*")
   picture = forms.FileField( label="Foto*")

class editData(forms.Form):
   name = forms.CharField(max_length=20,label="Nombre*")
   description = forms.CharField(max_length=200,label="Descripción*",widget=forms.Textarea)
   price = forms.CharField(max_length=5,label="Precio (€/día)*")
   status = forms.ChoiceField(choices=[(str(x),x.value) for x in Status], label="Estado*")

class editPicture(forms.Form):
   picture = forms.FileField( label="Foto*")