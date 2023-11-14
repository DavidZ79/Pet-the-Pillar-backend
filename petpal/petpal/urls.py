from django.urls import include, path
from django.contrib import admin
from account import urls as account_urls
from pet import urls as pet_urls
from notification import urls as notification_urls
from application import urls as application_urls
from comment import urls as comment_urls
from api import urls as api_urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Endpoints

# Authentication for users with tokens
# Create seeker and shelter
# Update seeker and shelter
# Get shelter
# Get shelter list
# Delete Shelter Seeker (implement cascading in models)

# PETS
# Create pet 
# Update pet
# Delete pet (implement cascading in models)
# Get pet
# Get pet search list (filtering sorting pagination)

# CHAT + REVIEWS (COMMENTS)
# Create chat message
# Create shelter review
# Get chat list (sort descending time)
# Get reviews list (sort descending time)

# APPLICATION
# Create application (pet must be available)
# Update applications
# Get shelter application list (filter sort pagination)
# Get application

# NOTIFICATIONS
# Create notification (not needed if done already in another action)
# Update notification (status read / unread)
# Get notification list (sort filter pagination)
# Delete notification
# Get notification

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('account/', include(account_urls)),
    # path('pet/', include(pet_urls)),
    # path('comment/', include(comment_urls)),
    # path('application/', include(application_urls)),
    # path('notification/', include(notification_urls)),

    path('api/', include(api_urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]