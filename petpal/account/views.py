from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer

class LoginView (generics.CreateAPIView):
   # serializer_class = ModelSerializer
   # def get (self, request):
   #    return 0
   pass

class RegisterView (generics.CreateAPIView):
   pass