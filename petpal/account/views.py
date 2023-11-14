from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from api.models import BaseUser, PetShelter, PetSeeker
from .serializer import UserSerializer, ShelterSerializer, SeekerSerializer
from django.contrib.auth import authenticate
from django.views.generic.edit import View
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializer import ShelterSerializer, SeekerSerializer, UserSerializer, LoginSerializer
from api.models import BaseUser, PetSeeker, PetShelter

class registerShelter(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        serializer.data['refresh_token'] = str(refresh)
        serializer.data['access_token'] = str(refresh.access_token)
        serializer.data['user_id'] = user.id

class registerSeeker(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = SeekerSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        serializer.data['refresh_token'] = str(refresh)
        serializer.data['access_token'] = str(refresh.access_token)
        serializer.data['user_id'] = user.id

class loginUser(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = get_user_model().objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'user_id': user.id
            }
            return Response(data)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
    
class TestView(View):
    def get(self, request):

        d = {"id": '1', "username": '2'}
        return JsonResponse(d)
