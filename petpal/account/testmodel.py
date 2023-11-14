from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class newUser (AbstractUser):
   name = models.CharField(max_length=30)
   email = models.EmailField(unique=True)
   phoneNumber = models.CharField(max_length=15, blank=True, null=True)
   location = models.CharField(max_length=255)
   picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True)
   password = models.CharField(max_length=100)

class PetShelter (newUser):
   missionStatement = models.TextField()
   rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
   # petListing = 

class PetSeeker (newUser):
   preference = models.CharField(max_length=200)