from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.hashers import check_password, make_password
from django import forms
from django.core.mail import EmailMessage
from datetime import date
import calendar
from django.conf import settings
import stripe
import requests
from django.db import IntegrityError

from user.models import User
from user.forms import Register, editPass, editUsername, editProfile, editPic, contact,descargaDatos, LoginForm
from payment.views import charge
from reviews.models import Comment
from rent.models import JuegosFav, Game, Rent

# Create your views here.

def profile(request, id_user):
    user = get_object_or_404(User, pk=id_user)
    list_comments = Comment.objects.filter(toUser=user)
    end = None

    drop = True

    # Comprobamos que no tiene alquileres pendientes antes de borrar sus datos
    if (request.user.is_authenticated):
        rents = Rent.objects.filter(user=request.user)
        games = Game.objects.filter(owner=request.user) 
        for x in rents:
            if(x.rentable == False):
                drop = False
                break
        request.session['drop'] = drop
        for x in games:
            rents1 = Rent.objects.filter(game=x)

            for y in rents1:
                if(y.rentable == False):
                    drop = False
                    break  
    
    key = settings.STRIPE_PUBLISHABLE_KEY
    if(not(request.user.is_anonymous)):
        if(request.user.premium):
            end = request.user.end_date.strftime('%d/%m/%Y')

    return render(request,'profile.html', {'user':user, 'comments': list_comments,'key':key,'premium_date':end})

def logout(request):
     do_logout(request)
     return redirect('/')

def login(request):
    # Creamos el formulario de autenticación vacío
    form = LoginForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = LoginForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

            form.add_error('username','El nombre de usuario o la contraseña no existen')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form})

def delete_myUSer(request, pk):

    # Recuperamos la instancia del user y la borramos
    instancia = User.objects.get(id=pk)
    if request.user.admin==False:
        drop = request.session['drop']

    # Comprobamos que está logueado el usuario o el administrador para poder borrar sus datos
    if(instancia == request.user or request.user.admin == True):
        
        if request.user.admin==False:
            if(drop == False):
                return profile(request,request.user.id)

        request.session['drop'] = True
        instancia.delete()
        if request.user.admin == True:
            return redirect('/users')
        return redirect('/')
    
    return redirect('/')

def new_user(request):

    if(request.method=='POST'):

        formulario = Register(request.POST ,request.FILES or None)
        
        if(formulario.is_valid()):
                
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            name = formulario.cleaned_data['name']
            last_name = formulario.cleaned_data['last_name']
            email = formulario.cleaned_data['email']
            bio = formulario.cleaned_data['bio']
            picture = ''
            address = formulario.cleaned_data['address']
            response = requests.get(
                'https://eu1.locationiq.com/v1/search.php?key=pk.bfdfa73760621b89cf9e8435ffcf48df&q=' + address + '&format=json')
            geodata = response.json()
            
            try:
                lat = float(geodata[0]['lat'])
                lon = float(geodata[0]['lon'])
            except:
                formulario.add_error('address', 'La dirección no existe')
                lat = 0.0
                lon = 0.0
            phone = formulario.cleaned_data['phone']

            if (password != formulario.cleaned_data['password2']):
                formulario.add_error('password2','No coinciden las contraseñas')

            try:
                user = User(username=username, password=password,first_name=name,last_name=last_name,email=email,bio=bio,picture=picture,phone=phone,address=address,lat=lat,lon=lon)
                if (len(formulario.errors) == 0):
                    user.set_password(user.password)
                    user.save()
                    favs = JuegosFav(user=user)
                    favs.save()
                    favs.items.set([])
                    favs.save()
                    do_login(request, user)
            except IntegrityError:
                formulario.add_error('username','Este nombre de usuario ya existe')

            if(len(formulario.errors)!=0):
                return render(request,"newuser.html",{"form":formulario})

            return redirect('/profile/{}'.format(user.id))

        else:

            #username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            #name = formulario.cleaned_data['name']
            #last_name = formulario.cleaned_data['last_name']
            bio = formulario.cleaned_data['bio']
            picture = ''
            address = formulario.cleaned_data['address']
            response = requests.get(
                'https://eu1.locationiq.com/v1/search.php?key=pk.bfdfa73760621b89cf9e8435ffcf48df&q=' + address + '&format=json')
            geodata = response.json()
            
            try:
                lat = float(geodata[0]['lat'])
                lon = float(geodata[0]['lon'])
            except:
                formulario.add_error('address', 'La dirección no existe')
                lat = 0.0
                lon = 0.0

            if (password != formulario.cleaned_data['password2']):
                formulario.add_error('password2','No coinciden las contraseñas')

            try:
                user = User(password=password,bio=bio,picture=picture,address=address,lat=lat,lon=lon)
                if (len(formulario.errors) == 0):
                    user.set_password(user.password)
                    user.save()
                    favs = JuegosFav(user=user)
                    favs.save()
                    favs.items.set([])
                    favs.save()
                    do_login(request, user)
            except IntegrityError:
                formulario.add_error('username','Este nombre de usuario ya existe')

            if(len(formulario.errors)!=0):
                return render(request,"newuser.html",{"form":formulario})

    else:

        formulario = Register()

    return render(request,"newuser.html",{"form":formulario})

def edit_pass(request):
    
    if(request.method=='POST'):
        formulario = editPass(request.POST)


        if(formulario.is_valid()):

            username = request.user.username
            password1 = formulario.cleaned_data['password3']
            user1 = authenticate(username=username, password=password1)
            
            if user1 is None:
                formulario.add_error('password3','Contraseña actual incorrecta')

            if(formulario.cleaned_data['password1']!=formulario.cleaned_data['password2']):
                formulario.add_error('password2','No coinciden las contraseñas')
            
            if(formulario.errors):
                return render(request,"newuser.html",{"form":formulario})

            password = make_password(formulario.cleaned_data['password1'])

            User.objects.filter(id=request.user.id).update(password=password)
            user = get_object_or_404(User,pk=request.user.id)

            do_logout(request)
            do_login(request, user)

            return redirect('/profile/{}'.format(user.id))

    else:
        formulario = editPass()

    return render(request,"newuser.html",{"form":formulario})

def edit_username(request):
    
    if(request.method=='POST'):
        formulario = editUsername(request.POST)


        if(formulario.is_valid()):

            username1 = request.user.username

            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password']

            user1 = authenticate(username=username1, password=password)
            
            if user1 is None:
                formulario.add_error('password','Contraseña actual incorrecta')

            if(formulario.errors):
                return render(request,"newuser.html",{"form":formulario})

            User.objects.filter(id=request.user.id).update(username=username)
            user = get_object_or_404(User,pk=request.user.id)

            do_logout(request)
            do_login(request, user)

            return redirect('/profile/{}'.format(user.id))

    else:
        formulario = editUsername()
        
        formulario.fields["username"].initial = request.user.username

    return render(request,"newuser.html",{"form":formulario})

def edit_profile(request):
    
    if(request.method=='POST'):
        formulario = editProfile(request.POST)


        if(formulario.is_valid()):
            
            if(formulario.errors):
                return render(request,"newuser.html",{"form":formulario})

            name = formulario.cleaned_data['name']
            last_name = formulario.cleaned_data['last_name']
            email = formulario.cleaned_data['email']
            bio = formulario.cleaned_data['bio']
            address = formulario.cleaned_data['address']
            response = requests.get(
                'https://eu1.locationiq.com/v1/search.php?key=pk.bfdfa73760621b89cf9e8435ffcf48df&q=' + address + '&format=json')
            geodata = response.json()
            try:
                lat = float(geodata[0]['lat'])
                lon = float(geodata[0]['lon'])
            except:
                formulario.add_error('address', 'La direccion no existe')
                lat = 0.0
                lon = 0.0
            phone = formulario.cleaned_data['phone']

            if(len(formulario.errors)!=0):
                return render(request,"newuser.html",{"form":formulario})

            User.objects.filter(id=request.user.id).update(first_name=name,last_name=last_name,email=email,bio=bio,phone=phone,address=address,lat=lat,lon=lon)

            return redirect('/profile/{}'.format(request.user.id))

    else:
        formulario = editProfile()

        formulario.fields["name"].initial = request.user.first_name
        formulario.fields["last_name"].initial = request.user.last_name
        formulario.fields["email"].initial = request.user.email
        formulario.fields["bio"].initial = request.user.bio
        formulario.fields["phone"].initial = request.user.phone
        formulario.fields["address"].initial = request.user.address

    return render(request,"newuser.html",{"form":formulario})

def edit_pic(request):

    user = get_object_or_404(User,pk=request.user.id)

    if request.method == "POST":
        form = editPic(request.POST,request.FILES or None)

        if form.is_valid():
            
            picture = form.cleaned_data['picture']

            user.picture = picture
            user.save()

            return redirect('/profile/{}'.format(request.user.id))
    else:
        form = editPic()

    return render(request, 'newuser.html', {'form': form})

def user_list(request):
    if(request.user.admin):
        users = User.objects.exclude(pk=request.user.id)
    else:
        users = []
    return render(request,'users.html',{'users':users})

def contact_user(request,pk):
    user = get_object_or_404(User, pk=pk)

    if request.method=='POST':
        form = contact(request.POST)
        if form.is_valid():
            title = 'Mensaje del administrador de TryOnBoard'
            body = form.cleaned_data['message'] + '\n'
            body += 'Comunicarse a: '+ user.email
            emailto = user.email

            email = EmailMessage(title,body,to=[emailto])
            email.send()
            return render(request,'index.html',{'mensaje': 'Se ha enviado correctamente el correo al usuario.'})
    else:
        form = contact()
    return render(request,'contact.html',{'form':form})

def DescargaDatosUser(request,pk):
    user = get_object_or_404(User, pk=pk)
    if(not(request.user == user)):
         return redirect('/')
    else:

        if request.method=='POST':
            form = descargaDatos(request.POST)
            if form.is_valid():
                title = 'Mensaje del administrador de TryOnBoard' 
                body = 'Aquí están los datos que TRY ON BOARD tiene sobre usted:' + '\n'

                body += 'Usuario:'+ user.username + '\n'
                body += 'Biografía:'+ user.bio + '\n'        
                body += 'Nombre:'+ user.first_name + '\n'
                body += 'Apellidos :'+ user.last_name + '\n'
                body += 'Email:'+ user.email + '\n'
                body += 'Dirección:'+ user.address + '\n'
                body += 'Teléfono:'+ user.phone + '\n'
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                     ip = request.META.get('REMOTE_ADDR')
                body += 'Direccion ip:'+ ip + '\n'
                body += '----------------------------------' + '\n'
                body += 'Mis juegos: ' + '\n'
                games = Game.objects.filter(owner=request.user)

                for x in games:
                    body += x.name + ' - ' + '['+ str(x.price) +']' + '\n'
                    body += 'Descripción: ' + x.description + '\n'
                    body += '\n'

                emailto = user.email
                

                email = EmailMessage(title,body,to=[emailto])
                #email.attach_file(user.picture.url)
                email.send()
                return render(request,'index.html',{'mensaje': 'Se ha enviado correctamente el correo con sus datos. ¡Gracias por confiar en Try on Board!'})
        else:
            form = descargaDatos()
        return render(request,'descargaDatos.html',{'form':form})

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: 
        m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d,month=m, year=y)

def premium(request):

    if(request.user.premium == False):
        
        #Claculamos la fecha fin
        months = int(request.POST.get('months')) 
        end = monthdelta(date.today(), months)
        
        #Realizamos el pago
        charge = stripe.Charge.create(
            amount=int(3.99*months*100),
            currency='eur',
            description='A Django charge',
            source=request.POST['stripeToken'],
            api_key=settings.STRIPE_SECRET_KEY) 

        #Actualizamos el usuario a usuario premium
        User.objects.filter(pk=request.user.id).update(premium=True,end_date=end)

    else:

        #Claculamos la nueva fecha fin
        months = int(request.POST.get('months')) 
        end = monthdelta(request.user.end_date, months)

        #Realizamos el pago
        charge = stripe.Charge.create(
            amount=int(3.99*months*100),
            currency='eur',
            description='A Django charge',
            source=request.POST['stripeToken'],
            api_key=settings.STRIPE_SECRET_KEY) 

        #Actualizamos al usuario con la nueva fecha fin
        User.objects.filter(pk=request.user.id).update(end_date=end)

    return redirect('/profile/{}'.format(request.user.id))
