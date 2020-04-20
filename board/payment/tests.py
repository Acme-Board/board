from django.test import TestCase
from django.utils.dateparse import parse_date
from user.models import User
from rent.models import Game, Status, Rent
from payment.models import Contend

class PaymentModelTestCase(TestCase):
    
    #Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user = User(username = 'prueba', password = 'prueba123')
        self.user.save()
        
        self.game = Game(name = 'BANG', description = 'Juego de mesa extremadamente satisfactorio', status = Status.PE, price = 22.5, picture = 'http://www.foto.com/foto.png', address = 'Los remedios', owner = self.user)
        self.game.save()

        self.rent = Rent(ticker = 'ABC-1234', days = 4, initial_date = parse_date("2020-07-13"), game = self.game, user = self.user, rentable = True)
        self.rent.save()

        self.contend = Contend(owner = self.user, rent = self.rent, status = 'Buen método de pago', description = 'El pago se efectua de forma segura', price = 55.75)
        self.contend.save()
      
    # Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):

        self.rent.delete()
        self.game.delete()
        self.user.delete()
        self.contend.delete()
