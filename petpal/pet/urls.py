from django.urls import path
from .views import CreatePetView

app_name = 'accounts'

urlpatterns = [
    path('create/', CreatePetView.as_view(), name='create-pet'),
]