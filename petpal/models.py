from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class PetShelter (models.Model):
   shelterName = models.CharField(max_length=30)
   email = models.CharField(max_length=200)
   address = models.CharField(max_length=200)
   phoneNum = models.CharField(max_length=100)
   userRating = models.IntegerField()
   petListing = 
   profilePic = 

class PetSeeker (models.Model):
   firstName = models.CharField(max_length=30)
   lastName = models.CharField(max_length=30)
   email = models.CharField(max_length=200)
   password = models.CharField(max_length=200)
   profilePic = 

class Animal (models.Model):
   name = models.CharField(max_length=25)
   characteristics = models.CharField(max_length=250)
   health = models.CharField(max_length=250)
   age = models.IntegerField()
   breed = models.CharField(max_length=25)
   gender = models.CharField(max_length=25)
   size = models.IntegerField()
   species = models.CharField(max_length=200)
   color = models.CharField(max_length=200)