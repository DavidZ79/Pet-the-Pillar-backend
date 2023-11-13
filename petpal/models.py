from django.db import models
from django.contrib.auth.models import User

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

class PetShelter (models.Model):
   shelterName = models.CharField(max_length=30)
   email = models.CharField(max_length=200)
   address = models.CharField(max_length=200)
   phoneNum = models.CharField(max_length=100)
   userRating = models.IntegerField()
   # petListing = 
   # profilePic = 

class PetSeeker (models.Model):
   firstName = models.CharField(max_length=30)
   lastName = models.CharField(max_length=30)
   email = models.CharField(max_length=200)
   password = models.CharField(max_length=200)
   # profilePic = 

class Pet (models.Model):
   name = models.CharField(max_length=25)
   description = models.TextField(max_lenngth=2500)
   characteristics = models.CharField(max_length=250)
   health = models.CharField(max_length=250)
   age = models.IntegerField()
   breed = models.CharField(max_length=25)
   gender = models.CharField(max_length=25)
   size = models.CharField()
   species = models.CharField(max_length=200)
   color = models.CharField(max_length=200)