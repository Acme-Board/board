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
        
        self.game = Game(name = 'BANG', description = 'Juego de mesa extremadamente satisfactorio', status = "Nuevo", price = 22.5, picture = 'http://www.foto.com/foto.png', owner = self.user)
        self.game.save()

        self.rent = Rent(ticker = 'ABC-1234', days = 4, initial_date = parse_date("2020-07-13"), game = self.game, user = self.user, rentable = True)
        self.rent.save()

        self.contend = Contend(owner = self.user, rent = self.rent, status = 'Buen método de pago', description = 'El pago se efectua de forma segura', price = 55.75)
        self.contend.save()
    
    #Batería de test unitarios ------------------------------------------------------------------------

    def test_get_owner(self):
        self.assertEquals(self.contend.owner, self.user)

    def test_get_rent(self):
        self.assertEquals(self.contend.rent, self.rent)

    def test_get_description(self):
        self.assertEquals(self.contend.description,'El pago se efectua de forma segura')

    def test_get_status(self):
        self.assertEquals(self.contend.status, 'Buen método de pago') 

    def test_get_price(self):
        self.assertEquals(self.contend.price, 55.75)
    
    def test_creation_contend(self):

        Contend(owner = self.user, rent = self.rent, status = 'Buen método de pago', description = 'El pago se efectua de forma segura', price = 55.75).save()

        contends = Contend.objects.all()
        self.assertEquals(contends.count(), 2)

    def test_edit_contend(self):

        Contend.objects.filter(id = self.contend.id).update(owner = self.user, rent = self.rent, status = 'Transferencia', description = 'Sus millones están en camino', price = 65.95)
        contend = Contend.objects.get(id = self.contend.id)

        self.assertEquals(contend.owner, self.user)
        self.assertEquals(contend.rent, self.rent)
        self.assertEquals(contend.status, 'Transferencia')
        self.assertEquals(contend.description, 'Sus millones están en camino')
        self.assertEquals(contend.price, 65.95)

    def test_delete_contend(self):

        self.contend2 = Contend(owner = self.user, rent = self.rent, status = 'Transferencia', description = 'Sus millones están en camino', price = 65.95)
        self.contend2.save()

        self.assertEquals(2, Contend.objects.count())
        self.contend2.delete()
        self.assertEquals(1, Contend.objects.count())
      
    
    # Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):

        self.rent.delete()
        self.game.delete()
        self.user.delete()
        self.contend.delete()
