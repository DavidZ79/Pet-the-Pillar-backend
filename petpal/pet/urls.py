from django.urls import path
from .views import CreatePetView

urlpatterns = [
    path('create/', CreatePetView.as_view(), name='create-pet'),
]
