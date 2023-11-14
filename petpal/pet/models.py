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
# class newUser(AbstractUser):
#     name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     phoneNumber = models.CharField(max_length=15, blank=True, null=True)
#     location = models.CharField(max_length=255)
#     picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True)
#     password = models.CharField(max_length=100)

#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         related_name="newuser_set",
#         related_query_name="newuser",
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="newuser_set",
#         related_query_name="newuser",
#     )


# class PetShelter(newUser):
#     missionStatement = models.TextField()
#     rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

class Photo(models.Model):
    image = models.ImageField(upload_to='photo_folder/')

class MorePhotos(models.Model):
    photos = models.ManyToManyField(Photo, blank=True)

class Pet(models.Model):
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=[("Adopted", "Adopted"), ("Pending", "Pending"), ("Available", "Available"), ("Withdrawn", "Withdrawn")])
    photos = models.ForeignKey(MorePhotos, on_delete=models.CASCADE)
   #  shelter = models.ForeignKey(PetShelter, on_delete=models.CASCADE)
    description = models.TextField(max_length=2500)
    behavior = models.TextField(max_length=2000)
    medicalHistory = models.TextField(max_length=2000)
    specialNeeds = models.TextField(max_length=2000)
    age = models.IntegerField()
    breed = models.CharField(max_length=25)
    gender = models.CharField(max_length=25)
    size = models.CharField(max_length=2, choices=[("S", "Small"), ("M", "Medium"), ("L", "Large"), ("XL", "Extra Large")])
    species = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    location = models.CharField(max_length=200)
    fee = models.IntegerField()
