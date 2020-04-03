import string
import random
from datetime import date, datetime

from django.shortcuts import render ,  get_object_or_404

from django.utils.dateparse import parse_date
from rent.models import Game , Rent, Status

from django.conf import settings
from rent.forms import NewGame, editData, editPicture
from django.shortcuts import redirect

# Create your views here.
from rent.models import Rent
from rent.models import Order
from rent.models import OrderItem
from user.models import User


def games_list(request):
    if(request.user.is_authenticated):
        games = Game.objects.exclude(owner=request.user)
    else:
        games = Game.objects.all()
    return render(request,'games.html',{'games':games})

def games_list_by_user(request):
    games = Game.objects.filter(owner=request.user)
    return render(request,'myGames.html',{'myGames':games})

def games_list_by_zona(request,zona):
    games = Game.objects.filter(zona=zona)
    return render(request,'games.html',{'games':games})

def games_list_by_status(request,status):
    games = []
    filtro = True
    
    if (int(status)==1):
        games = Game.objects.filter(status="Perfecto")
    if (int(status)==2):
        games = Game.objects.filter(status="Faltan piezas")
    if (int(status)==3):
        games = Game.objects.filter(status="Gastado")
    if (int(status)==4):
        games = Game.objects.filter(status="Injugable")
    
    return render(request,'games.html',{'games':games,'filter':filtro})

def rents_list(request):
    rents  = Rent.objects.filter(user = request.user)
    return render(request,'rents.html',{'rents':rents})


def games_detail(request,pk):
     dato = get_object_or_404(Game, pk=pk)
     return render(request,'gameDetail.html', {'name':dato.name, 'description':dato.description,'price': dato.price ,
      'status': dato.status,'picture' : dato.picture, 'id' : dato.id,'owner': dato.owner })

def delete(request, pk):
    # Recuperamos la instancia de la persona y la borramos
    instancia = Game.objects.get(id=pk)
    instancia.delete()

    # Después redireccionamos de nuevo a la lista
    return redirect('/')

def new_game(request):
    texto = "Subida de "
    Alquilar = "Subir Juego"
    if request.method == "POST":
        form = NewGame(request.POST,request.FILES or None)
        
        if form.is_valid():

            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']

            if(status == "Status.PE"):
                status = "Perfecto"
            
            if(status == "Status.FA"):
                status = "Faltan piezas"
            
            if(status == "Status.GA"):
                status = "Gastado"
            
            if(status == "Status.IN"):
                status = "Injugable"

            try:
                price = float(form.cleaned_data['price'])
            except ValueError:
                form.add_error('price','Introduzca un dato numérico')
                return render(request,"newgame.html",{"form":form, 'texto': texto, 'Alquilar': Alquilar})

            if (price < 0):
                form.add_error('price','No puede ser un precio negativo')
                return render(request,"newgame.html",{"form":form, 'texto': texto, 'Alquilar': Alquilar})
            
            if price==0:
                form.add_error('price','No se puede regalar un juego')
                return render(request,"newgame.html",{"form":form , 'texto': texto, 'Alquilar': Alquilar}) 

            picture = form.cleaned_data['picture']
            address = form.cleaned_data['address']
            owner = request.user
            game = Game(name=name,description=description,status=status,price=price,picture=picture,address=address,owner=owner)

            game.save()
            return redirect('/gameDetail/{}'.format(game.id))
    else:
       form = NewGame()
    return render(request, 'newgame.html', {'form': form, 'texto': texto, 'Alquilar': Alquilar})
    
def edit_game(request, pk):
    texto = "Editar "
    Alquilar = "Actualizar"
    juego = get_object_or_404(Game, pk=pk)

    if request.method == "POST":
        form = editData(request.POST,request.FILES or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']

            if(status == "Status.PE"):
                status = "Perfecto"
            
            if(status == "Status.FA"):
                status = "Faltan piezas"
            
            if(status == "Status.GA"):
                status = "Gastado"
            
            if(status == "Status.IN"):
                status = "Injugable"

            try:
                price = float(form.cleaned_data['price'])
            except ValueError:
                form.add_error('price','Introduzca un dato numérico')
                return render(request,"newgame.html",{"form":form, 'texto': texto, 'Alquilar': Alquilar})

            if (price < 0):
                form.add_error('price','No puede ser un precio negativo')
                return render(request,"newgame.html",{"form":form, 'texto': texto, 'Alquilar': Alquilar})
            
            if price==0:
                form.add_error('price','No se puede regalar un juego')
                return render(request,"newgame.html",{"form":form, 'texto': texto, 'Alquilar': Alquilar}) 

            address = form.cleaned_data['address']

            Game.objects.filter(pk=pk).update(name=name,description=description,status=status,price=price,address=address)

            return redirect('/gameDetail/{}'.format(pk))
    else:
        form = editData()
        form.fields["name"].initial = juego.name
        form.fields["description"].initial = juego.description
        form.fields["status"].initial = juego.status
        form.fields["price"].initial = juego.price
        form.fields["address"].initial = juego.address
    return render(request, 'newgame.html', {'form': form, 'texto': texto, 'Alquilar': Alquilar})

def edit_pic(request, pk):
    juego = get_object_or_404(Game, pk=pk)

    if request.method == "POST":
        form = editPicture(request.POST,request.FILES or None)

        if form.is_valid():
            
            picture = form.cleaned_data['picture']

            Game.objects.filter(pk=pk).update(picture=picture)

            return redirect('/gameDetail/{}'.format(pk))
    else:
        form = editPicture()

        form.fields["picture"].initial = juego.picture

    return render(request, 'newgame.html', {'form': form, 'texto': texto, 'Alquilar': Alquilar})

def rent_game(request, id_game, days, initial):
    dato = get_object_or_404(Game, pk=id_game)
    user = get_object_or_404(User, pk=request.user.id)
    letters = string.ascii_uppercase
    digits = string.digits
    ramdomLetters = ''.join(random.choice(letters) for i in range(3))
    ramdomNumber = ''.join(random.choice(digits) for i in range(4))
    ticker = ramdomLetters + '-' + ramdomNumber
    rent = Rent(ticker=ticker, game=dato,days = days, initial_date=initial, user= user, rentable=False)
    rent.save()


def rents_list(request,id_user):
    rents = Rent.objects.filter(user=request.user)
    return render(request,'rents.html',{'rents':rents})

def view_cart(request):
    user = get_object_or_404(User, pk=request.user.id)
    list_carts = Order.objects.filter(user=user)
    if not list_carts:
        ramdomLetters = ''.join(random.choice(string.ascii_uppercase) for i in range(4))
        ramdomNumber = ''.join(random.choice(string.digits) for i in range(5))
        ref = ramdomLetters + '-' + ramdomNumber
        cart = Order(ref_code=ref, user=user, actual=True)
        cart.save()
        return render(request, 'orders.html', {'order': cart.items.all(), 'sum':cart.get_total_price(), 'id':cart.id})
    else:
        for c in list_carts:
            if c.actual:
                cart = c
                return render(request, 'orders.html', {'order': cart.items.all(),'sum':cart.get_total_price(), 'id':cart.id})

def add_item_to_cart(request, id_game):
    dato = get_object_or_404(Game, pk=id_game)
    user = get_object_or_404(User, pk=request.user.id)
    list_carts = Order.objects.filter(user=user)
    days = 1
    initial = None
    if request.method == "POST":
        if request.POST.get("days") is None:
            dato = get_object_or_404(Game, pk=id_game)
            return render(request, 'gameDetail.html',
                      {'name': dato.name, 'description': dato.description, 'price': dato.price,
                       'status': dato.status, 'picture': dato.picture, 'id': dato.id, 'owner': dato.owner})
        if int(request.POST.get("days")) <=0:
            dato = get_object_or_404(Game, pk=id_game)
            return render(request, 'gameDetail.html',
                          {'name': dato.name, 'description': dato.description, 'price': dato.price,
                           'status': dato.status, 'picture': dato.picture, 'id': dato.id, 'owner': dato.owner})
        days = request.POST.get("days")
        #Fecha inicio
        if request.POST.get("initial") is None:
            dato = get_object_or_404(Game, pk=id_game)
            return render(request, 'gameDetail.html',
                      {'name': dato.name, 'description': dato.description, 'price': dato.price,
                       'status': dato.status, 'picture': dato.picture, 'id': dato.id, 'owner': dato.owner})
        if parse_date(request.POST.get("initial")) < datetime.date(datetime.now()):
            dato = get_object_or_404(Game, pk=id_game)
            return render(request, 'gameDetail.html',
                          {'name': dato.name, 'description': dato.description, 'price': dato.price,
                           'status': dato.status, 'picture': dato.picture, 'id': dato.id, 'owner': dato.owner})
        initial = parse_date(request.POST.get("initial"))
    if not list_carts:
        ramdomLetters = ''.join(random.choice(string.ascii_uppercase) for i in range(4))
        ramdomNumber = ''.join(random.choice(string.digits) for i in range(5))
        ref = ramdomLetters + '-' + ramdomNumber
        cart = Order(ref_code=ref, user=user, actual=True)
        cart.save()
        añadir = True
        for item in cart.items.all():
            if item.game == dato:
                añadir = False
                break
        if añadir:
            item = OrderItem(game=dato, days=days, initial_date=initial, is_ordered=False, date_added=date.today())
            item.save()
            cart.items.add(item)
            cart.save()
        return render(request, 'orders.html', {'order': cart.items.all(), 'id':cart.id, 'mensaje': 'Añadido con exito','sum':cart.get_total_price()})
    else:
        for c in list_carts:
            if c.actual:
                cart = c
                añadir = True
                for item in cart.items.all():
                    if item.game == dato:
                        añadir = False
                        return render(request, 'orders.html', {'order': cart.items.all(), 'id':cart.id, 'mensaje': 'Item ya incluido en el carrito','sum':cart.get_total_price()})
                    if item.game.owner == user:
                        añadir = False
                        return render(request, 'orders.html', {'order': cart.items.all(), 'id':cart.id, 'mensaje': 'No puedes comprar tu propio juego','sum':cart.get_total_price()})
                if añadir:
                    item = OrderItem(game=dato, days=days, initial_date=initial, is_ordered=False, date_added=date.today())
                    item.save()
                    cart.items.add(item)
                    cart.save()
                return render(request, 'orders.html', {'order': cart.items.all(), 'id':cart.id, 'mensaje': 'Añadido con exito','sum':cart.get_total_price()})

def delete_item_from_cart(request, id_item):
    dato = get_object_or_404(OrderItem, pk=id_item)
    user = get_object_or_404(User, pk=request.user.id)
    list_carts = Order.objects.filter(user=user)
    for c in list_carts:
        if c.actual:
            cart = c
            for item in cart.items.all():
                if item == dato:
                    cart.items.remove(item)
                    dato.delete()
                    return render(request, 'orders.html', {'order': cart.items.all(), 'id':cart.id, 'mensaje': 'Eliminado con exito','sum':cart.get_total_price()})
    return redirect('/cart')

def empty_cart(request):
    user = get_object_or_404(User, pk=request.user.id)
    list_carts = Order.objects.filter(user=user)
    for c in list_carts:
        if c.actual:
            cart = c
            for item in cart.items.all():
                cart.items.remove(item)
                item.delete()
    return render(request, 'orders.html', {'order': cart.items.all(), 'id':cart.id, 'mensaje': 'Carrito vaciado','sum':cart.get_total_price()})
