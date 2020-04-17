from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator, validate_comma_separated_integer_list
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    bio = models.TextField(max_length=500)
    range = models. CharField(max_length=10)
    picture = models.FileField(upload_to='board/staticfiles/media/myfolder/',null=True)
    rate = models. CharField(max_length=10, validators=[validate_comma_separated_integer_list])
    address = models.TextField(max_length=500)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17)  # validators should be a list
    admin = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    end_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.first_name