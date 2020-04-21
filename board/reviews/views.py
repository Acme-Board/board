from django.shortcuts import render, get_object_or_404, redirect
from django.db import DataError
# Create your views here.
from reviews.forms import ReviewForm
from reviews.models import Valoration, Comment
from user.models import User

from rent.models import Rent, Game


def create_review(request, id_user):
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            rate = form.cleaned_data['valoration']
            com = form.cleaned_data['comment']
            if 0.0 <= float(rate) <= 5.0:
                fromUser = get_object_or_404(User, pk=request.user.id)
                toUser = get_object_or_404(User, pk=id_user)
                rent_list_from = Rent.objects.filter(user=fromUser)
                rent_list_to = Rent.objects.filter(user=toUser)
                games_from = Game.objects.filter(owner=fromUser)
                games_to = Game.objects.filter(owner=toUser)
                #Voy a comprobar si ambos usuarios comparten un alquiler
                existRent = False
                if rent_list_from:
                    for rent in rent_list_from:
                        for game in games_to:
                            if rent.game == game:
                                existRent = True
                                break
                if rent_list_to:
                    for rent in rent_list_to:
                        for game in games_from:
                            if rent.game == game:
                                existRent = True
                                break
                if existRent:
                    valoration = Valoration(fromUser=fromUser, toUser=toUser, rate=rate)
                    comment = Comment(fromUser=fromUser, toUser=toUser, comment=com)
                    valoration.save()
                    comment.save()
                    list_valoration = Valoration.objects.filter(toUser=toUser)
                    suma = 0.0
                    numero = 0
                    for valor in list_valoration:
                        suma = suma + valor.rate
                        numero = numero + 1
                    media = suma/numero
                    toUser.rate = media
                    try:
                        toUser.save()
                    except DataError:
                        return redirect('/profile/{}'.format(toUser.id))  
                    
                    return redirect('/profile/{}'.format(toUser.id))
                else:
                    return render(request, "createReview.html", {'form': form, 'mensaje': 
                    'Necesitas haber alquilado algun producto del Usuario para poder darle una valoración'})

            else:
                return render(request, "createReview.html", {'form': form})
    return render(request, "createReview.html", {'form': form})

def list_comments(request, id_user):
    toUser = get_object_or_404(User, pk=id_user)
    list_comments = Comment.objects.filter(toUser=toUser)
    return render(request, "comments.html", {'comments': list_comments})
