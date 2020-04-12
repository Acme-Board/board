from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from rent.models import Game, Order, Rent
from user.models import User
from rent.views import rent_game, empty_cart
from payment.models import Contend
from payment.forms import newContend
import stripe
from django.core.mail import EmailMessage

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

def new_contend(request,pk):
    rent = get_object_or_404(Rent,pk=pk)

    if request.method == "POST":
        form = newContend(request.POST)

        if form.is_valid():
            
            description = form.cleaned_data['description']
            status = 'PENDING'

            contend = Contend(owner=request.user,rent=rent,status=status,description=description)
            contend.save()

            return redirect('/myGames/')
    else:
        form = newContend()

    return render(request, 'newContend.html', {'form': form})

def contend_list(request):
    contends = Contend.objects.all()
    return render(request, 'contends.html', {'contends':contends})

def contend_detail(request,pk):
    contend = get_object_or_404(Contend, pk=pk)
    return render(request,'contendDetail.html', {'contend':contend})

def new_compensation(request,pk):
    price = request.POST.get('price')
    contend = get_object_or_404(Contend,pk=pk)

    #Contend
    Contend.objects.filter(id=pk).update(price=price,status='ACCEPTED')

    #Message
    title = 'Mensaje del administrador de TryOnBoard' 
    body = 'Usted ha recibido una disputa.' + '\n'

    body += 'Usuario que abrió la disputa:'+ contend.owner.username + '\n'
    body += 'Sobre el juego que alquiló:'+ '\n'       
    body += contend.rent.ticker + '\n'
    body += 'Nombre del juego:'+ contend.rent.game.name + '\n'
    body += 'Indemnización puesta por el administrador:'+ price + '\n'
    emailto = contend.rent.user.email
    
    email = EmailMessage(title,body,to=[emailto])
    email.send()

    return redirect('/contends/')