from django.urls import path
from . import views

app_name = 'notification'

# NOTIFICATIONS
# Create notification (not needed if done already in another action)
# Update notification (status read / unread)
# Get notification list (sort filter pagination)
# Delete notification
# Get notification

# Notifications
#   User
#   Status: Read, Unread
#   Forward (Application, Pet, Review, Chat) 
#           Users should receive notifications for messages, status updates, and new pet listings (based on their preference).
#           Shelters should receive notification for new reviews, new applications, and new messages from applicants.
#   Timestamp
#   Content

urlpatterns = [
    path('', views.NotificationCreateAPI.as_view(), name="notification_create"),
    path('<int:notification_id>/', views.NotificationAPI.as_view(), name="notification_api"),
    path('list/<int:user_id>/', views.NotificationListAPI.as_view(), name="notification_list"),
]