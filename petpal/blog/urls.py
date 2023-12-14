from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', BlogCreateAPI.as_view(), name='blog-create'),
    path('<int:blog_id>', BlogAPI.as_view(), name='view-blog'),
    path('list/<int:shelter_id>', BlogListAPI.as_view(), name='blog-list'),
    path('list2/<int:shelter_id>', BlogListAPI2.as_view(), name='blog-list'),
]