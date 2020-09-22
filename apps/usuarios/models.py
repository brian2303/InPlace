from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    image = models.ImageField(upload_to='image_users', null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
