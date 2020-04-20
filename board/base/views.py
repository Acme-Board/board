from django.shortcuts import render
from django.conf import settings
# Create your views here.

def base(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request,'base.html', {'key':key})

def index(request):
    return render(request,'index.html') 

def terms(request):
    return render(request,'terms.html') 

def privacy(request):
    return render(request,'privacy.html') 