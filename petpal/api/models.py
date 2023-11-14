from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
#           Users should receive notifications for messages, status updates, and new pet listings (based on their preference).
#           Shelters should receive notification for new reviews, new applications, and new messages from applicants.
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
class BaseUser (AbstractUser):
   name = models.CharField(max_length=30)
   email = models.EmailField(unique=True)
   phoneNumber = models.CharField(max_length=15, blank=True, null=True)
   location = models.CharField(max_length=255)
   picture = models.ImageField(upload_to='user_pictures/', blank=True, null=True)
   password = models.CharField(max_length=100)
   groups = models.ManyToManyField(
      'auth.Group',
      verbose_name='groups',
      blank=True,
      help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
      related_name="newuser_set",
      related_query_name="newuser",
    )
   user_permissions = models.ManyToManyField(
      'auth.Permission',
      verbose_name='user permissions',
      blank=True,
      help_text='Specific permissions for this user.',
      related_name="newuser_set",
      related_query_name="newuser",
    )
   

class PetShelter (BaseUser):
   # base = models.OneToOneField
   missionStatement = models.TextField()
   rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
   # petListing = 

class PetSeeker (BaseUser):
   preference = models.CharField(max_length=200)

class Photo (models.Model):
   images = models.ImageField(upload_to='photo_folder/')

class MorePhotos(models.Model):
    # Other fields in your model
    photos = models.ManyToManyField(Photo, blank=True)
    # Other fields in your model

class Pet (models.Model):
   name = models.CharField(max_length=30)
   status = models.CharField(max_length=10,choices=[("Adopted", "Adopted"), ("Pending", "Pending"), ("Available", "Available"), ("Withdrawn", "Withdrawn")])
   # note: profilePic = make pfp the first pic of the photos
   photos = models.ForeignKey(MorePhotos, on_delete=models.CASCADE)
   shelter = models.ForeignKey(PetShelter, on_delete=models.CASCADE)
   description = models.TextField(max_length=2500)
   behavior = models.CharField(max_length=2000)
   medicalHistory = models.CharField(max_length=2000)
   specialNeeds = models.CharField(max_length=2000)
   age = models.IntegerField()
   breed = models.CharField(max_length=25)
   gender = models.CharField(max_length=25)
   size = models.CharField(max_length=2, choices=[("S", "S"), ("M", "M"),("L", "L"),("XL", "XL")])
   species = models.CharField(max_length=200)
   color = models.CharField(max_length=200)
   timestamp = models.DateTimeField(auto_now_add=True)
   location = models.CharField(max_length=200)
   fee = models.IntegerField()

class Application (models.Model):
   status = models.CharField(max_length=10, choices=[("Accepted", "Accepted"), ("Pending", "Pending"), ("Denied", "Denied")])
   reason = models.CharField(max_length=2000)
   seeker = models.ForeignKey(PetSeeker, on_delete=models.CASCADE)
   pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

class Comment (models.Model):
   content = models.CharField(max_length=2000)
   timestamp = models.DateTimeField(auto_now_add=True)
   user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

   class Meta:
      abstract = True

class Chat (Comment):
   application = models.ForeignKey(Application, on_delete=models.CASCADE)

class Review (Comment):
   # shelter = models.ForeignKey(PetShelter, on_delete=models.CASCADE)
   rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


class Notification (models.Model):
   user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

   status = models.CharField(max_length=10, choices=[("Read", "Read"), ("Unread", "Unread")])
   
   # forward = models.ForeignKey(Pet, Application, Review)
   content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
   object_id = models.PositiveBigIntegerField()
   content_object = GenericForeignKey()

   timestamp = models.DateTimeField(auto_now_add=True)
   content = models.CharField(max_length=2000)
