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
    path('review/<int:shelter_id>/list/<int:parent_id>/', views.ReviewListAPI.as_view(), name="review_shelter_list"),
    path('review/detail/<int:review_id>/', views.SingleReviewAPI.as_view(), name="single_review_detail"),
    path('discussion/detail/<int:discussion_id>/', views.SingleDiscussionAPI.as_view(), name="single_discussion_detail"),
    path('discussion/<int:blog_id>/', views.DiscussionAPI.as_view(), name="discussion_blog_create"),
    path('discussion/<int:blog_id>/list/<int:parent_id>/', views.DiscussionListAPI.as_view(), name="discussion_blog_list"),
    path('rating/<int:shelter_id>/', views.RatingAPI.as_view(), name="rating_api"),
    path('likes/<int:blog_id>/', views.LikesAPI.as_view(), name="likes_api"),
    # path('likes/<int:blog_id>/list/', views.LikesAPI.as_view(), name="likes_api"),
]