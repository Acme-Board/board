from django import forms
from .models import Contend

class newContend(forms.Form):
   description = forms.CharField(max_length=300,label="Descripción",widget=forms.Textarea)
