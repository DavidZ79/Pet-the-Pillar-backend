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
    path('chat/<int:application_id>/', views.ChatAPI.as_view(), name="chat_application_create"),
    path('chat/<int:application_id>/list/', views.ChatListAPI.as_view(), name="chat_application_list"),
    path('review/<int:shelter_id>/', views.ReviewAPI.as_view(), name="review_shelter_create"),
    path('review/<int:shelter_id>/list/', views.ReviewListAPI.as_view(), name="review_shelter_list"),
]