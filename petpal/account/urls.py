from django.urls import path
from . import views
from .views import registerUser, registerSeeker, registerShelter, login

app_name="account"

urlpatterns = [
    # path('api/login/', views.LoginView.as_view(), name='login'),
    path('login/', login, name='login'),
    # path('api/register/', views.RegisterView.as_view(), name='register')
    path('register/user/', registerUser, name='register_user'),
    path('register/shelter/', registerShelter, name='register_pet_shelter'),
    path('register/seeker/', registerSeeker, name='register_pet_seeker'),

    path('test/', views.TestView.as_view(), name='testView')
]