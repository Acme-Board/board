from django import forms


class ReviewForm(forms.Form):
    valoration = forms.ChoiceField(choices=[('0',0),('1',1),('2',2),('3',3),('4',4),('5',5)], label="Valoración")
    comment = forms.CharField(max_length=500, required = True, label='Comentario', widget=forms.Textarea)