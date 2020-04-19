from django.test import TestCase

from user.models import User
from reviews.models import Valoration, Comment

class ValorationModelTestCase(TestCase):
    
    #Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user1 = User(username='prueba', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5',
        lat=2.5,lon=3.0)
        self.user1.save()

        self.user2 = User(username='prueba1', password='prueba123', first_name='Gonzalo', last_name='Aguilar', email='zalo@gmail.com', 
        bio='Me gusta jugar a cosas entretenidas', picture='http://www.foto.com/foto.png', range='Pro', rate='2.5',
        lat=2.5,lon=3.0)
        self.user2.save()

        self.valoration = Valoration(toUser=self.user1, fromUser=self.user2, rate=2.5)
        self.valoration.save()

        self.comment = Comment(toUser=self.user1, fromUser=self.user2, comment='Buen juego, mejor jugador')
        self.comment.save()
    
    #Batería de test unitarios ------------------------------------------------------------------------

    def test_get_valoration_toUser(self):
        self.assertEquals(self.valoration.toUser, self.user1)
    
    def test_get_valoration_fromUser(self):
        self.assertEquals(self.valoration.fromUser, self.user2)

    def test_get_valoration_rate(self):
        self.assertEquals(self.valoration.rate, 2.5)   

    def test_get_comment_toUser(self):
        self.assertEquals(self.comment.toUser, self.user1)

    def test_get_comment_fromUser(self):
        self.assertEquals(self.comment.fromUser, self.user2)

    def test_get_comment_comment(self):
        self.assertEquals(self.comment.comment, 'Buen juego, mejor jugador')             

    #Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):
        self.valoration.delete()
        self.comment.delete()
        self.user1.delete()
        self.user2.delete()