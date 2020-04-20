import random
from django.test import TestCase
from django.utils.dateparse import parse_date
from user.models import User
from rent.models import Game, Status, Rent, OrderItem, Order
from datetime import date, datetime , timedelta
from rent import views as rent_views

class GameModelTestCase(TestCase):
    
    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):
        self.user = User(username='prueba001', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5',lat=2.5,lon=3.0)
        self.user.save()
        
        self.game = Game(name='BANG', description='descripcion', status='Nuevo', price=2.5, picture='http://www.foto.com/foto.png', owner=self.user)
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

    def test_edit_game(self):

        Game.objects.filter(id = self.game.id).update(name = 'Party', description = 'Muy entretenido', status = Status.PE, price = 1.5, picture = 'http://www.party.com/party.png', owner = self.user)
        game = Game.objects.get(id = self.game.id)

        self.assertEquals(game.name, 'Party')
        self.assertEquals(game.description, 'Muy entretenido')
        self.assertEquals(game.price, 1.5)
        self.assertEquals(game.picture, 'http://www.party.com/party.png')
        self.assertEquals(game.owner, self.user)

    def test_delete_game(self):

        self.game2 = Game(name = 'Party', description = 'Muy entretenido', status = Status.PE, price = 1.5, picture = 'http://www.party.com/party.png', owner = self.user)
        self.game2.save()

        self.assertEquals(2, Game.objects.count())
        self.game2.delete()
        self.assertEquals(1, Game.objects.count())           
               
    # Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):

        self.rent.delete()
        self.game.delete()
        self.user.delete()

class RentModelTestCase(TestCase):

    # Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

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

    def test_edit_rent(self):

        Rent.objects.filter(id = self.rent.id).update(ticker = 'LMN-1234', game = self.game, days = 5, initial_date = parse_date("2020-07-13"), user = self.user2, rentable = False, deliver = True)
        rent = Rent.objects.get(id = self.rent.id)

        self.assertEquals(rent.ticker, 'LMN-1234')
        self.assertEquals(rent.game, self.game)
        self.assertEquals(rent.days, 5)
        self.assertEquals(rent.user, self.user2)
        self.assertEquals(rent.rentable, False)
        self.assertEquals(rent.deliver, True)

    def test_delete_rent(self):

        self.rent2 = Rent(ticker = 'LMN-1234', game = self.game, days = 5, initial_date = parse_date("2020-07-13"), user = self.user2, rentable = False, deliver = True)
        self.rent2.save()

        self.assertEquals(2, Rent.objects.count())
        self.rent2.delete()
        self.assertEquals(1, Rent.objects.count())

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

        self.game = Game(name='BANG', description='Está muy entretenido', status=Status.PE, price=2.5, picture='http://www.foto.com/foto.png', owner=self.user)
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

    def test_edit_orderItem(self):

        self.game2 = Game(name = 'Cluedo', description = 'Resulta muy chulo', status = Status.PE, price = 4.5, picture = 'http://www.foto.com/foto.png', owner = self.user)
        self.game2.save()

        OrderItem.objects.filter(id = self.orderItem.id).update(game = self.game2, date_added = parse_date("2020-09-20"), days =15, initial_date = parse_date("2020-11-25"))
        orderItem = OrderItem.objects.get(id = self.orderItem.id)

        self.assertEquals(orderItem.game, self.game2)
        # self.assertEquals(orderItem.date_added, parse_date("2020-09-20"))
        self.assertEquals(orderItem.days, 15)
        # self.assertEquals(orderItem.initial_date, parse_date("2020-11-25"))

    def test_delete_orderItem(self):

        self.orderItem2 = OrderItem(game = self.game, is_ordered = False, date_added = parse_date("2020-10-12"), days = 3, initial_date = parse_date("2020-10-15"))
        self.orderItem2.save()

        self.assertEquals(2, OrderItem.objects.count())
        self.orderItem2.delete()
        self.assertEquals(1, OrderItem.objects.count())

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

        self.game = Game(name='BANG', description='Está muy entretenido', status=Status.PE, price=2.5, picture='http://www.foto.com/foto.png', owner=self.user)
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

    def test_edit_order(self):

        Order.objects.filter(id = self.order.id).update(ref_code= 'VBNM-12345', user = self.user, actual = False, date_ordered = parse_date("2020-10-10"))
        order = Order.objects.get(id = self.order.id)

        self.assertEquals(order.ref_code, 'VBNM-12345')
        self.assertEquals(order.user, self.user)
        self.assertEquals(order.actual, False)
        # self.assertEquals(order.date_ordered, "2020-10-10")

    def test_delete_order(self):

        self.order2 = Order(ref_code= 'EFGH-12345', user = self.user, actual = True, date_ordered = parse_date("2020-07-13"))
        self.order2.save()

        self.assertEquals(2, Order.objects.count())
        self.order2.delete()
        self.assertEquals(1, Order.objects.count())

    # Borra los datos para terminar con los test ------------------------------------------------------

    def tearDown(self):

        self.game.delete()
        self.user.delete()
        self.order.delete()
        self.orderItem.delete()
