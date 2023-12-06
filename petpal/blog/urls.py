from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    # path('', ApplicationCreateView.as_view(), name='blog-create'),
    # path('<int:blog_id>', ApplicationCreateView.as_view(), name='view-blog'),
    # path('list/<int:shelter_id', ApplicationListView.as_view(), name='blog-list'),
]