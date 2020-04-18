from django.test import TestCase

from user.models import User
from reviews.models import Valoration, Comment
from reviews import views as reviews_views

class ReviewModelTestCase(TestCase):
    
    #Prepara una bbdd default con los objetos que se van a testear en este TestCase -------------------

    def setUp(self):

        self.user1 = User(username='prueba1',password='prueba123')
        self.user1.save()

        self.user2 = User(username='prueba2',password='prueba456')
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

    def test_list_comments(self):

        self.assertEquals(1, Comment.objects.count())

        self.comment = Comment(toUser=self.user2, fromUser=self.user1, comment='Amazing game')
        self.comment.save()

        self.assertEquals(2, Comment.objects.count())

    def test_list_valorations(self):

        self.assertEquals(1, Valoration.objects.count())

        self.valoration = Valoration(toUser=self.user2, fromUser=self.user1, rate=2.5)
        self.valoration.save()

        self.assertEquals(2, Valoration.objects.count())

    def test_edit_comment(self):

        Comment.objects.filter(id = self.comment.id).update(comment='Bueno... resulta ameno sino tienes electricidad') 
        comment = Comment.objects.get(id = self.comment.id)

        self.assertEquals(comment.comment, 'Bueno... resulta ameno sino tienes electricidad')

    def test_edit_valoration(self):

        Valoration.objects.filter(id = self.valoration.id).update(rate=5.0) 
        valoration = Valoration.objects.get(id = self.valoration.id)

        self.assertEquals(valoration.rate, 5.0)

    def test_delete_comment(self):

        self.comment2 = Comment(toUser=self.user1, fromUser=self.user2, comment='Buen juego, buen jugador')
        self.comment2.save()

        self.assertEquals(2, Comment.objects.count())
        self.comment2.delete()
        self.assertEquals(1, Comment.objects.count())

    def test_delete_valoration(self):

        self.valoration2 = Valoration(toUser=self.user1, fromUser=self.user2, rate=3.5)
        self.valoration2.save()

        self.assertEquals(2, Valoration.objects.count())
        self.valoration2.delete()
        self.assertEquals(1, Valoration.objects.count())

    #Borra los datos para terminar con los test ------------------------------------------------------
    
    def tearDown(self):
        self.valoration.delete()
        self.comment.delete()
        self.user1.delete()
        self.user2.delete()