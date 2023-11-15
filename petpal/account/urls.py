from django.urls import path
from . import views
from .views import registerShelter, loginUser, registerSeeker, AllShelterListView, ShelterProfileView, SeekerProfileView, PetSeekerUpdateView, PetShelterUpdateView

app_name="account"

urlpatterns = [
    path('register/shelter/', registerShelter.as_view(), name='register'),
    path('register/seeker/', registerSeeker.as_view(), name='seeker'),
    path('login/', loginUser.as_view(), name='login'),

    path('shelter/<int:id>/', ShelterProfileView.as_view(), name='shelterprofile'),
    path('seeker/<int:id>/', SeekerProfileView.as_view(), name='seekerprofile'),

    path('shelter/<int:pk>/update/', PetShelterUpdateView.as_view(), name='shelterupdate'),
    path('seeker/<int:pk>/update/', PetSeekerUpdateView.as_view(), name='seekerupdate'),

    
    path('all/shelter/', AllShelterListView.as_view(), name='shelterview'),
    # remove this later
    path('all/', views.AllListView.as_view(), name='allview'),
    path('all/seeker/', views.AllSeekerListView.as_view(), name='seekerview'),

]