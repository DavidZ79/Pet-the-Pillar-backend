from django.urls import path
from .views import *

app_name = 'application'

urlpatterns = [
    path('', ApplicationCreateView.as_view(), name='application-create'),
    path('<int:application_id>/update/', ApplicationCreateView.as_view(), name='update_application'),
    path('list/', ApplicationListView.as_view(), name='application-list')
]