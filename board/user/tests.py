from django.test import TestCase

from user.models import User
from user.forms import editAccount
from user.forms import editProfile
from user.forms import editProfile
from user import views as user_views

class UserModelTestCase(TestCase):

    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user = User(username='prueba', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5')
        self.user.save()       

    # Batería de test unitarios ------------------------------------------------------------------------

    def test_get_username(self):
        self.assertEquals(self.user.username, 'prueba')

    def test_get_password(self):
        self.assertEquals(self.user.password, 'prueba123')   

    def test_get_firstName(self):
        self.assertEquals(self.user.first_name, 'Gonzalo')

    def test_get_lastName(self):
        self.assertEquals(self.user.last_name, 'Aguilar')

    def test_get_email(self):
        self.assertEquals(self.user.email, 'zalo@gmail.com')    

    def test_get_bio(self):
        self.assertEquals(self.user.bio, 'Me gusta jugar a cosas entretenidas')  

    def test_get_picture(self):
        self.assertEquals(self.user.picture, 'http://www.foto.com/foto.png')    

    def test_get_range(self):
        self.assertEquals(self.user.range, 'Pro')   

    def test_get_rate(self):
        self.assertEquals(self.user.rate, '2.5')     

    def test_edit_user(self):
        self.assertEquals(1,User.objects.count())
        user_views.delete_myUSer(self,self.user.id)
        self.assertEqual(0,User.objects.count())       

    # Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):
        self.user.delete()

'''
class RegisterFormTestCase(TestCase):

    def setUp(self):

        self.register = Register(username='gonzaloguiher', password1='P@$$w0rd', password2='P@$$w0rd', name='Gonzalo', last_name='Aguilar', 
        email='zalo@gmail.com', bio='Soy un chico divertido, extrovertido y graciosillo', picture='http://www.foto.com/foto.png', check = True)

        self.register.save()

 # Batería de test unitarios ------------------------------------------------------------------------

    def test_get_username(self):
        self.assertEquals(self.register.username, 'gonzaloguiher')

    def test_get_password1(self):
        self.assertEquals(self.register.password1, 'P@$$w0rd')  

    def test_get_password2(self):
        self.assertEquals(self.register.password2, 'P@$$w0rd') 

    def test_get_name(self):
        self.assertEquals(self.register.name, 'Gonzalo')

    def test_get_lastName(self):
        self.assertEquals(self.register.last_name, 'Aguilar')

    def test_get_email(self):
        self.assertEquals(self.register.email, 'zalo@gmail.com')    

    def test_get_bio(self):
        self.assertEquals(self.register.bio, 'Me gusta jugar a cosas entretenidas')  

    def test_get_picture(self):
        self.assertEquals(self.register.picture, 'http://www.foto.com/foto.png')

    # Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):
        self.register.delete()'''