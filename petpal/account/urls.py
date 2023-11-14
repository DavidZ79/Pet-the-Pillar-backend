from django.urls import path
from . import views

app_name="account"
urlpatterns = [
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/register/', views.RegisterView.as_view(), name='register')
]