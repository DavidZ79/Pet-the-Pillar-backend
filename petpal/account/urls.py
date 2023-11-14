from django.urls import path
from . import views
from .views import registerUser, registerSeeker, registerShelter, login

app_name="account"
urlpatterns = [
    # path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/login/', login, name='login'),
    # path('api/register/', views.RegisterView.as_view(), name='register')
    path('api/register/user/', registerUser, name='register_user'),
    path('api/register/shelter/', registerShelter, name='register_pet_shelter'),
    path('api/register/seeker/', registerSeeker, name='register_pet_seeker'),
]