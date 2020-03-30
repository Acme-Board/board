from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator, validate_comma_separated_integer_list

# Create your models here.

class User(AbstractUser):
    bio = models.TextField(max_length=500)
    range = models. CharField(max_length=10)
    picture = models.FileField(upload_to='board/staticfiles/media/myfolder/',blank=True,null = True )
    rate = models. CharField(max_length=10, validators=[validate_comma_separated_integer_list])
    admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name