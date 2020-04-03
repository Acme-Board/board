from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from rent.models import Game, Order
from rent.views import rent_game, empty_cart
import stripe

def pay(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request,'home.html',{'key':key})

def charge(request,id_cart):
    cart = get_object_or_404(Order, pk=id_cart)
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=int(cart.get_total_price()*100),
            currency='eur',
            description='A Django charge',
            source=request.POST['stripeToken'],
            api_key=settings.STRIPE_SECRET_KEY
        )
        for item in cart.items.all():
            rent_game(request,item.game.id, item.days, item.initial_date)
        #rent_game(request,id_game)
        return redirect('/success/')

def pago_completado(request):
    empty_cart(request)
    return render(request,'pago_completado.html')

def confirm(request,id_cart):
    cart = get_object_or_404(Order, pk=id_cart)
    sum = cart.get_total_price()
    key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request,'aceptacion_pago.html',{'order':cart.get_cart_items(), 'id':cart.id,'key':key, 'cent':int(sum*100), 'total':sum}) 