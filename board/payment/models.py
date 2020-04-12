from django.db import models
from user.models import User
from rent.models import Rent

# Create your models here.

class Contend(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    rent = models.ForeignKey(Rent,on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    description = models.TextField(max_length=500)
    price = models.FloatField(null=True)    

    @classmethod
    def get_by_id(cls, cid):
        return Contend.objects.get(pk=cid)    

    def __unicode__(self):
        return '{}-{}'.format(self.owner.username,self.rent.ticker)

    def __str__(self):
        return '{}-{}'.format(self.owner.username,self.rent.ticker)