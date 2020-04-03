from django.db import models
from enum import Enum, auto
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator

from user.models import User

# Create your models here.

class Status(Enum):
    PE = 'Perfecto'
    FA = 'Faltan piezas'
    GA = 'Gastado'
    IN = 'Injugable'

class Game(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.TextField(max_length=500, default='')
    status = models.CharField(max_length=20)
    price = models.FloatField(help_text="El precio del alquiler equivaldrá a 1 día", validators=[MinValueValidator(0.1,"No puede regalar un juego"),MinValueValidator(0.0,"No puedue ser negativo")])
    picture = models.FileField(upload_to='board/staticfiles/media/myfolder/',blank=True,null = True )
    address = models.CharField(max_length=100, default='')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    

    @classmethod
    def get_by_id(cls, cid):
        return Game.objects.get(pk=cid)    

    def __unicode__(self):
        return '{}-{}'.format(self.name,self.price)

    def __str__(self):
        return self.name

    def is_rentable(self):
        return Rent.objects.get(game=self).rentable

class Rent(models.Model):
    ticker = models.CharField(max_length=8, default='ABC-1234')
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    initial_date = models.DateTimeField(null=False)
    days = models.IntegerField(default=1, validators=[MinValueValidator(1, "No puedes alquilarlo menos de un dia")])
    rentable = models.BooleanField(default=True)

    @classmethod
    def get_by_id(cls, cid):
        return Rent.objects.get(pk=cid) 
    
    def __unicode__(self):
        return '{}[{}]'.format(self.ticker,self.game)

    def __str__(self):
        return self.ticker

class OrderItem(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    days = models.IntegerField(default=1, validators=[MinValueValidator(1, "No puedes alquilarlo menos de un dia")])
    initial_date = models.DateTimeField(null=False)

    def __str__(self):
        return self.game.name

class Order(models.Model):
    ref_code = models.CharField(max_length=10, default='ABCD-12345')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    items = models.ManyToManyField(OrderItem, blank=True)
    actual = models.BooleanField(default=True) #Especifica si es el carrito actual o ya a sido pedido
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.ref_code

    def get_cart_items(self):
        return self.items.all()
    
    def get_total_price(self):
        sum = 0
        for x in self.get_cart_items():
            sum = sum + (x.game.price * x.days)
        return sum
