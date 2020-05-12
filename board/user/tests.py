from django.test import TestCase

from user.models import User
from user.forms import editProfile
from user import views as user_views

class UserModelTestCase(TestCase):

    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user = User(username='prueba', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5',
        lat=2.5,lon=3.0)
        
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

    def test_edit_account(self):

        User.objects.filter(id = self.user.id).update(username = 'username', password = 'password') 
        user = User.objects.get(id = self.user.id)

        self.assertEquals(user.username, 'username')
        self.assertEquals(user.password, 'password')

    def test_edit_profile(self):

        User.objects.filter(id=self.user.id).update(first_name = 'Antonio', last_name = 'Macías', email = 'antmaczam@gmail.com', bio = 'Soy un chico divertido, extrovertido y graciosillo')
        user = User.objects.get(id = self.user.id)

        self.assertEquals(user.first_name, 'Antonio')
        self.assertEquals(user.last_name, 'Macías')
        self.assertEquals(user.email, 'antmaczam@gmail.com')
        self.assertEquals(user.bio, 'Soy un chico divertido, extrovertido y graciosillo') 
    
    def test_edit_picture(self):

        User.objects.filter(pk = self.user.id).update(picture = 'http://www.picture.com/picture.png')
        user = User.objects.get(id = self.user.id)

        self.assertEquals(user.picture, 'http://www.picture.com/picture.png')

    # Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):
        self.user.delete()
