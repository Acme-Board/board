from django.shortcuts import render

from rent.models import Order

# Create your views here.

def base(request):
    return render(request,'base.html')

def index(request):
    if(request.user.is_authenticated):
        list_carts = Order.objects.filter(user=request.user)
        if(not list_carts):
            request.session['cart'] = 0
        else:
            for c in list_carts:
                if c.actual:
                    cart = c
                    request.session['cart'] = cart.items.count()
    return render(request,'index.html') 

def terms(request):
    return render(request,'terms.html') 

def privacy(request):
    return render(request,'privacy.html') 