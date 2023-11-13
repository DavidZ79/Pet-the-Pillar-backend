from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# User
#   Email
#   Phone Number
#   Password
#   Picture
#   Name
#   Location
#   Note: Referenced by Animal, Application
#   Seeker:
#       Preference
#   Shelter:
#       Mission Statement
#       Rating
# Pet
#   Name
#   Status (Adopted, Pending, Available, Withdrawn)
#   Photos (GRRR ME ANGRY)
#   Shelter (REFERENCE)
#   Description
#   Behavior
#   Medical History
#   Special needs
#   Age
#   Breed
#   Gender
#   Size
#   Species
#   Color
#   Timestamp
#   Location
#   Fee
# Application
#   Status: Pending, Accepted, Denied
#   Reason
#   Seeker (REFERENCE)
#   Pet (REFERENCE)
# Notifications
#   User
#   Status: Read, Unread
#   Forward (Application, Pet, Review)
#   Timestamp
#   Content
# Comment
#   Content
#   Timestamp
#   User (REFERENCE) 
#   Chat
#     Application (REFERENCE)
#   Review
#     Shelter
#     Rating
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

class Photo (models.Model):
   images = models.ImageField(upload_to='photo_folder/')

class MorePhotos(models.Model):
    # Other fields in your model
    photos = models.ManyToManyField(Photo, blank=True)
    # Other fields in your model

class Pet (models.Model):
   name = models.CharField(max_length=30)
   status = models.CharField(choices=[("Adopted", "Adopted"), ("Pending", "Pending"), ("Available", "Available"), ("Withdrawn", "Withdrawn")])
   # note: profilePic = make pfp the first pic of the photos
   photos = models.ForeignKey(MorePhotos)
   shelter = models.ForeignKey(PetShelter)
   description = models.TextField(max_lenngth=2500)
   behavior = models.CharField(max_length=2000)
   medicalHistory = models.CharField(max_length=2000)
   specialNeeds = models.CharField(max_length=2000)
   age = models.IntegerField(max_length=3)
   breed = models.CharField(max_length=25)
   gender = models.CharField(max_length=25)
   size = models.CharField(max_length=2, choices=[("S", "S"), ("M", "M"),("L", "L"),("XL", "XL")])
   species = models.CharField(max_length=200)
   color = models.CharField(max_length=200)
   timestamp = models.DateTimeField()
   location = models.CharField(max_length=200)
   fee = models.IntegerField()

class Application (models.Model):
   status = models.CharField(choices=[("Accepted", "Accepted"), ("Pending", "Pending"), ("Denied", "Denied")])
   reason = models.CharField(max_length=2000)
   seeker = models.ForeignKey(PetSeeker)
   pet = models.ForeignKey(Pet)

class Comment (models.Model):
   content = models.CharField(max_length=2000)
   timestamp = models.DateTimeField()
   user = models.ForeignKey(newUser)

class Chat (Comment):
   application = models.ForeignKey(Application)

class Review (Comment):
   shelter = models.ForeignKey(PetShelter)
   rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


class Notification (models.Model):
   user = User
   status = models.CharField(choices=[("Read", "Read"), ("Unread", "Unread")])
   forward = models.ForeignKey(Pet, Application, Review)
   timestamp = models.DateTimeField()
   content = models.CharField(max_length=2000)
