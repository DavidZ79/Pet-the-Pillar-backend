from django.urls import path
from . import views
# from .views import registerUser, registerSeeker, registerShelter, login
from .views import registerShelter, TestView, loginUser, registerSeeker

app_name="account"

urlpatterns = [
    # path('register/shelter/', views.registerShelter.as_view(), name='register'),

    path('register/shelter/', registerShelter.as_view(), name='register'),
    path('register/seeker/', registerSeeker.as_view(), name='seeker'),
    path('login/', loginUser.as_view(), name='login'),

    path('test/', views.TestView.as_view(), name='testView'),

]