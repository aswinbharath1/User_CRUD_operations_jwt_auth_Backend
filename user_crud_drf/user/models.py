from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length= 255)
    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(upload_to='profileImg/',null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    username = models.CharField(max_length= 255,null=True,blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']