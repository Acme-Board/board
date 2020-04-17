from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.hashers import check_password, make_password
from django import forms
from django.core.mail import EmailMessage
from django.db import IntegrityError

from user.models import User
from user.forms import Register, editAccount, editProfile, editPic, contact

from reviews.models import Comment


# Create your views here.

def profile(request, id_user):
     user = get_object_or_404(User, pk=id_user)
     list_comments = Comment.objects.filter(toUser=user)
     return render(request,'profile.html', {'user':user, 'comments': list_comments})

def logout(request):
     do_logout(request)
     return redirect('/')

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
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

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form})

def delete_myUSer(request, pk):

    # Recuperamos la instancia del user y la borramos
    instancia = User.objects.get(id=pk)
    
    if(instancia == request.user or request.user.admin == True):
        instancia.delete()
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
            
            if (password != formulario.cleaned_data['password2']):
                formulario.add_error('password2','No coinciden las contraseñas')

            try:
                user = User(username=username, password=password,first_name=name,last_name=last_name,email=email,bio=bio,picture=picture)
                user.set_password(user.password)
                user.save()
                do_login(request, user)
            except IntegrityError:
                formulario.add_error('username','Este nombre de usuario ya existe')

            if(len(formulario.errors)!=0):
                return render(request,"newuser.html",{"form":formulario})

            return redirect('/profile/{}'.format(user.id))

    else:

        formulario = Register()

    return render(request,"newuser.html",{"form":formulario})

def edit_account(request):
    
    if(request.method=='POST'):
        formulario = editAccount(request.POST)


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

            username = formulario.cleaned_data['username']
            password = make_password(formulario.cleaned_data['password1'])

            User.objects.filter(id=request.user.id).update(username=username, password=password)
            user = get_object_or_404(User,pk=request.user.id)

            do_logout(request)
            do_login(request, user)

            return redirect('/profile/{}'.format(user.id))

    else:
        formulario = editAccount()
        
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

            User.objects.filter(id=request.user.id).update(first_name=name,last_name=last_name,email=email,bio=bio)

            return redirect('/profile/{}'.format(request.user.id))

    else:
        formulario = editProfile()

        formulario.fields["name"].initial = request.user.first_name
        formulario.fields["last_name"].initial = request.user.last_name
        formulario.fields["email"].initial = request.user.email
        formulario.fields["bio"].initial = request.user.bio

    return render(request,"newuser.html",{"form":formulario})

def edit_pic(request):

    if request.method == "POST":
        form = editPic(request.POST,request.FILES or None)

        if form.is_valid():
            
            picture = form.cleaned_data['picture']

            User.objects.filter(pk=request.user.id).update(picture=picture)

            return redirect('/profile/{}'.format(request.user.id))
    else:
        form = editPic()

    return render(request, 'newuser.html', {'form': form})

def user_list(request):
    if(request.user.admin):
        games = User.objects.exclude(pk=request.user.id)
    else:
        games = []
    return render(request,'users.html',{'users':games})

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
            return redirect('/')
    else:
        form = contact()
    return render(request,'contact.html',{'form':form})
def DescargaDatosUser(request,pk):
    user = get_object_or_404(User, pk=pk)
    if(not(request.user == user)):
         return redirect('/')
    else:

        if request.method=='POST':
            form = contact(request.POST)
            if form.is_valid():
                title = 'Mensaje del administrador de TryOnBoard' 
                body = 'Aqui estan los datos que TRY ON BOARD tiene sobre usted:' + '\n'

                body += 'Username:'+ user.username + '\n'
                body += 'Password:'+ user.password + '\n'
                body += 'Bio:'+ user.bio + '\n'        
                body += 'Name:'+ user.first_name + '\n'
                body += 'Last name :'+ user.last_name + '\n'
                body += 'Email:'+ user.email + '\n'
                emailto = user.email
                

                email = EmailMessage(title,body,to=[emailto])
                #email.attach_file(user.picture.url)
                email.send()
                return redirect('/')
        else:
            form = contact()
        return render(request,'descargaDatos.html',{'form':form})