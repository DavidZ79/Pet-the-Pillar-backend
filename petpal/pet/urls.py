from django.urls import path
from .views import ManagePetView, SearchPetView, ListPetView

app_name = 'pet'

urlpatterns = [
    path('', ManagePetView.as_view(), name='create-pet'),
    path('<int:pet_id>/', ManagePetView.as_view(), name='manage-pet'),
    path('list/', SearchPetView.as_view(), name='search-pets'),
    path('all/', ListPetView.as_view(), name='all-pets'),
]