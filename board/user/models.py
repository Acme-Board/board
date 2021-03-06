from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator, validate_comma_separated_integer_list
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    bio = models.TextField(max_length=500)
    range = models. CharField(max_length=10)
    picture = models.FileField(upload_to='board/staticfiles/media/myfolder/',null=True)
    rate = models. CharField(max_length=10, default=0, validators=[validate_comma_separated_integer_list])
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    address = models.TextField(max_length=500)
    phone_regex = RegexValidator(regex=r'^[0-9].{9,}$',
                                 message="El numero de telefono deben ser entre 9 y 10 digitos")
    phone = models.CharField(validators=[phone_regex], max_length=10)  # validators should be a list
    admin = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    end_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.first_name
  