import random
from django.test import TestCase
from django.utils.dateparse import parse_date
from user.models import User
from rent.models import Game, Status, Rent
from datetime import date, datetime , timedelta


class GameModelTestCase(TestCase):
    
    #Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):
        self.user = User(username='prueba001', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5',
        lat=2.5,lon=3.0)
        self.user.save()
        
        self.game = Game(name='BANG', description='descripcion', status='Nuevo', price=2.5, picture='http://www.foto.com/foto.png', owner=self.user)
        self.game.save()

        self.rent = Rent(ticker='ABC-1234', days=4, initial_date=parse_date("2020-07-13"), game=self.game, user=self.user, rentable=True)
  
        self.rent.save()
    
    #Batería de test unitarios ------------------------------------------------------------------------

    def test_get_owner(self):
        self.assertEquals(self.game.owner, self.user)
    
    def test_get_name(self):
        self.assertEquals(self.game.name,'BANG')

    def test_get_description(self):
        self.assertEquals(self.game.description,'descripcion')  

    def test_get_status(self):
        self.assertEquals(self.game.status, 'Nuevo') 

    def test_get_price(self):
        self.assertEquals(self.game.price, 2.5)

    def test_get_picture(self):
        self.assertEquals(self.game.picture, 'http://www.foto.com/foto.png') 

    def test_get_ticker(self):
        self.assertEquals(self.rent.ticker, 'ABC-1234')  

    def test_get_game(self):
        self.assertEquals(self.rent.game, self.game)     

    def test_get_user(self):
        self.assertEquals(self.rent.user, self.user)  

    def test_get_rentable(self):
        self.assertEquals(self.rent.rentable, True)              
               
    #Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):
        self.rent.delete()
        self.game.delete()
        self.user.delete()


class RentModelTestCase(TestCase):

    def setUp(self):
        self.user = User(username='prueba', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5',
        lat=2.5,lon=3.0)
        self.user.save()

        self.user2 = User(username='prueba2', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5',
        lat=2.5,lon=3.0)
        self.user2.save()

        self.game = Game(name='BANG', description='descripcion', status='Nuevo', price=2.5,
                         picture='http://www.foto.com/foto.png', owner=self.user)
        self.game.save()

        self.rent = Rent(ticker='WWW-1234', game=self.game, days=4, initial_date=parse_date("2020-07-13"), user=self.user2, rentable=True)
        self.rent.save()

    def test_get_ticker(self):
        self.assertEquals(self.rent.ticker, 'WWW-1234')

    def test_get_game(self):
        self.assertEquals(self.rent.game, self.game)

    def test_get_user(self):
        self.assertEquals(self.rent.user, self.user2)

    def test_get_rentable(self):
        self.assertEquals(self.rent.rentable, True)

    def test_get_days(self):
        self.assertEquals(self.rent.days, 4)

    def test_get_date(self):
        self.assertEquals(self.rent.initial_date, parse_date("2020-07-13"))

    def tearDown(self):
        self.rent.delete()
        self.game.delete()
        self.user.delete()
        self.user2.delete()