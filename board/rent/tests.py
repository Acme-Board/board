import random
from django.test import TestCase
from django.utils.dateparse import parse_date
from user.models import User
from rent.models import Game, Status, Rent, OrderItem, Order
from datetime import date, datetime , timedelta


class GameModelTestCase(TestCase):
    
    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):
        self.user = User(username='prueba', password='prueba123')
        self.user.save()
        
        self.game = Game(name='BANG', description='descripcion', status=Status.PE, price=2.5, picture='http://www.foto.com/foto.png', address='Los remedios', owner=self.user)
        self.game.save()

        self.rent = Rent(ticker='ABC-1234', days=4, initial_date=parse_date("2020-07-13"), game=self.game, user=self.user, rentable=True)
        self.rent.save()
   
    # Batería de test unitarios ------------------------------------------------------------------------

    def test_get_owner(self):
        self.assertEquals(self.game.owner, self.user)
    
    def test_get_name(self):
        self.assertEquals(self.game.name,'BANG')

    def test_get_description(self):
        self.assertEquals(self.game.description,'descripcion')  

    def test_get_status(self):
        self.assertEquals(self.game.status, Status.PE) 

    def test_get_price(self):
        self.assertEquals(self.game.price, 2.5)

    def test_get_picture(self):
        self.assertEquals(self.game.picture, 'http://www.foto.com/foto.png') 

    def test_get_address(self):
        self.assertEquals(self.game.address, 'Los remedios')

    def test_get_ticker(self):
        self.assertEquals(self.rent.ticker, 'ABC-1234')  

    def test_get_game(self):
        self.assertEquals(self.rent.game, self.game)     

    def test_get_user(self):
        self.assertEquals(self.rent.user, self.user)  

    def test_get_rentable(self):
        self.assertEquals(self.rent.rentable, True)           
               
    # Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):

        self.rent.delete()
        self.game.delete()
        self.user.delete()

class RentModelTestCase(TestCase):

    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user1 = User(username = 'prueba001', password = 'prueba123')
        self.user1.save()

        self.user2 = User(username = 'prueba002', password = 'prueba234')
        self.user2.save()

        self.game = Game(name = 'BANG', description = 'descripcion', status = Status.PE, price = 2.5, picture = 'http://www.foto.com/foto.png', address = 'Los remedios', owner = self.user1)
        self.game.save()

        self.rent = Rent(ticker = 'DFG-1234', game = self.game, days = 4, initial_date = parse_date("2020-07-13"), user = self.user2, rentable = True, deliver = False)
        self.rent.save()

    # Batería de test unitarios ------------------------------------------------------------------------

    def test_get_ticker(self):
        self.assertEquals(self.rent.ticker, 'DFG-1234')

    def test_get_game(self):
        self.assertEquals(self.rent.game, self.game)

    def test_get_user(self):
        self.assertEquals(self.rent.user, self.user2)

    def test_get_rentable(self):
        self.assertEquals(self.rent.rentable, True)

    def test_get_deliver(self):
        self.assertEquals(self.rent.deliver, False)

    def test_get_days(self):
        self.assertEquals(self.rent.days, 4)

    def test_get_date(self):
        self.assertEquals(self.rent.initial_date, parse_date("2020-07-13"))

    # Borra los datos para terminar con los test ------------------------------------------------------

    def tearDown(self):

        self.rent.delete()
        self.game.delete()
        self.user1.delete()
        self.user2.delete()

class OrderItemModelTestCase(TestCase):

    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user = User(username='prueba001', password='prueba123')
        self.user.save()

        self.game = Game(name='BANG', description='Está muy entretenido', status=Status.PE, price=2.5, picture='http://www.foto.com/foto.png', address='Los remedios', owner=self.user)
        self.game.save()

        self.orderItem = OrderItem(game=self.game, is_ordered=False, date_added = parse_date("2020-07-13"), days =10, initial_date = parse_date("2020-07-13"))
        self.orderItem.save()

    # Batería de test unitarios ------------------------------------------------------------------------

    def test_get_game(self):
        self.assertEquals(self.orderItem.game, self.game)

    def test_get_is_ordered(self):
        self.assertEquals(self.orderItem.is_ordered, False)

    def test_get_days(self):
        self.assertEquals(self.orderItem.days, 10)

    def test_get_initial_date(self):
        self.assertEquals(self.orderItem.initial_date, parse_date("2020-07-13"))

    # Borra los datos para terminar con los test ------------------------------------------------------

    def tearDown(self):

        self.game.delete()
        self.user.delete()
        self.orderItem.delete()

class OrderModelTestCase(TestCase):

    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user = User(username='prueba001', password='prueba123')
        self.user.save()

        self.game = Game(name='BANG', description='Está muy entretenido', status=Status.PE, price=2.5, picture='http://www.foto.com/foto.png', address='Los remedios', owner=self.user)
        self.game.save()

        self.orderItem = OrderItem(game=self.game, is_ordered=False, days =10, initial_date=parse_date("2020-07-13"))
        self.orderItem.save()

        self.order = Order(ref_code= 'EFGH-12345', user = self.user, actual = True, date_ordered = parse_date("2020-07-13"))
        self.order.save()

    # Batería de test unitarios ------------------------------------------------------------------------

    def test_get_ref_code(self):
        self.assertEquals(self.order.ref_code, 'EFGH-12345')

    def test_get_user(self):
        self.assertEquals(self.order.user, self.user)

    def test_get_actual(self):
        self.assertEquals(self.order.actual, True)

    def test_get_date_ordered(self):
        self.assertEquals(self.order.date_ordered, parse_date("2020-07-13"))

    # Borra los datos para terminar con los test ------------------------------------------------------

    def tearDown(self):

        self.game.delete()
        self.user.delete()
        self.order.delete()
        self.orderItem.delete()