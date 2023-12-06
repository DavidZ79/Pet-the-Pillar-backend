from django.urls import path, include
from account import urls as account_urls
from pet import urls as pet_urls
from notification import urls as notification_urls
from application import urls as application_urls
from comment import urls as comment_urls
from blog import urls as blog_urls
from . import views

app_name="api"

urlpatterns = [
    path('account/', include(account_urls)),
    path('pet/', include(pet_urls)),
    path('comment/', include(comment_urls)),
    path('application/', include(application_urls)),
    path('notification/', include(notification_urls)),
    path('blog/', include(blog_urls)),
]