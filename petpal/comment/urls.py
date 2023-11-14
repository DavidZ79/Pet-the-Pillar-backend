from django.urls import path
from . import views

app_name="comment"

# CHAT + REVIEWS (COMMENTS)
# Create chat message
# Create shelter review
# Get chat list (sort descending time)
# Get reviews list (sort descending time)

# Comment
#   Content
#   Timestamp
#   User (REFERENCE) 
#   Chat
#     Application (REFERENCE)
#   Review
#     Shelter
#     Rating
urlpatterns = [
    path('chat/', views.ChatAPI.as_view()),
    path('chat/list/', views.ChatListAPI.as_view()),
    path('review/', views.ReviewAPI.as_view()),
    path('review/list.', views.ReviewListAPI.as_view()),
]