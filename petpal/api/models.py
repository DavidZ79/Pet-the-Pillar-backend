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
#   Forward (Application, Pet, Review, Chat) 
#           Users should receive notifications for messages, status updates, and new pet listings (based on their preference).
#           Shelters should receive notification for new reviews, new applications, and new messages from applicants.
#   Timestamp
#   ContentnewUser"
# Comment
#   Content
#   Timestamp
#   User (REFERENCE) 
#   Chat
#     Application (REFERENCE)
#   Review
#     Shelter
#     Rating

class Notification (models.Model):
   # user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
   user_content_type = models.ForeignKey(ContentType, related_name="user", on_delete=models.CASCADE)
   user_object_id = models.PositiveBigIntegerField()
   user = GenericForeignKey("user_content_type", "user_object_id")

   status = models.CharField(max_length=10, choices=[("Read", "Read"), ("Unread", "Unread")])
   
   # forward = models.ForeignKey(Pet, Application, Review)
   forward_content_type = models.ForeignKey(ContentType, related_name="forward",on_delete=models.CASCADE)
   forward_object_id = models.PositiveBigIntegerField()
   forward = GenericForeignKey("forward_content_type", "forward_object_id")

   timestamp = models.DateTimeField(auto_now_add=True)
   content = models.CharField(max_length=2000)
   
   class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=["forward_content_type", "forward_object_id"]),
            models.Index(fields=["user_content_type", "user_object_id"]),
        ]

class BaseUser (AbstractUser):
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']

   username = models.CharField(max_length=30)
   email = models.EmailField(blank=True, unique=True)
   phoneNumber = models.CharField(max_length=15, blank=True, null=True)
   location = models.CharField(max_length=255)
   picture = models.ImageField(upload_to="user_pictures/", blank=True, null=True)
   password = models.CharField(max_length=100)
   notifications = GenericRelation(Notification, content_type_field="user_content_type", object_id_field="user_object_id")

   def is_pet_shelter(self):
      return hasattr(self, 'petshelter')
   
   def is_pet_seeker(self):
      return hasattr(self, 'petseeker')

class PetShelter (BaseUser):
   # base = models.OneToOneField(BaseUser, related_name="pet_shelter", on_delete=models.CASCADE)
   missionStatement = models.TextField()
   totalRating = models.IntegerField(blank=True, default=0)
   numberOfRating = models.IntegerField(blank=True,default=0)
   # petListing = 

class PetSeeker (BaseUser):
   # base = models.OneToOneField(BaseUser, related_name="pet_seeker", on_delete=models.CASCADE)
   preference = models.CharField(max_length=200)

class Photo (models.Model):
   image = models.ImageField(upload_to="photo_folder/")

class Pet (models.Model):
   name = models.CharField(max_length=30)
   status = models.CharField(max_length=10,choices=[("Adopted", "Adopted"), ("Pending", "Pending"), ("Available", "Available"), ("Withdrawn", "Withdrawn")])
   photos = models.ManyToManyField(Photo, blank=True)
   shelter = models.ForeignKey(PetShelter, on_delete=models.CASCADE)
   description = models.TextField(max_length=2500)
   behavior = models.CharField(max_length=2000)
   medicalHistory = models.CharField(max_length=2000)
   specialNeeds = models.CharField(max_length=2000)
   age = models.PositiveIntegerField()
   breed = models.CharField(max_length=25)
   gender = models.CharField(max_length=25)
   size = models.PositiveIntegerField(choices=[(0, "Extra Small"),(1, "Small"), (2, "Medium"),(3, "Large"),(4, "Extra Large")])
   species = models.CharField(max_length=50)
   color = models.CharField(max_length=50)
   timestamp = models.DateTimeField(auto_now_add=True)
   location = models.CharField(max_length=50)
   fee = models.IntegerField()

class Application (models.Model):
   status = models.CharField(max_length=10, choices=[("Accepted", "Accepted"), ("Pending", "Pending"), ("Denied", "Denied"), ("Withdrawn", "Withdrawn")])
   reason = models.CharField(max_length=2000)
   seeker = models.ForeignKey(PetSeeker, on_delete=models.CASCADE)
   pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
   timestamp = models.DateTimeField(auto_now_add=True)
   last_updated = models.DateTimeField(auto_now_add=True)

   class Meta:
      ordering = ['timestamp','last_updated']

class Comment (models.Model):
   content = models.CharField(max_length=2000)
   timestamp = models.DateTimeField(auto_now_add=True)

   # user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
   user_content_type = models.ForeignKey(ContentType, related_name="comment_user", on_delete=models.CASCADE)
   user_object_id = models.PositiveIntegerField()
   user = GenericForeignKey("user_content_type", "user_object_id")

   class Meta:
      abstract = True
      ordering = ['-timestamp']
      indexes = [
         models.Index(fields=["user_content_type", "user_object_id"]),
      ]

class Chat (Comment):
   user_content_type = models.ForeignKey(ContentType, related_name="chat_user", on_delete=models.CASCADE)
   
   application = models.ForeignKey(Application, on_delete=models.CASCADE)

class Review (Comment):
   user_content_type = models.ForeignKey(ContentType, related_name="review_user", on_delete=models.CASCADE)

   shelter = models.ForeignKey(PetShelter, related_name="review_shelter", on_delete=models.CASCADE)
   rating = models.IntegerField(blank=True, null=True)
