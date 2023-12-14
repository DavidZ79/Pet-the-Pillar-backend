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
from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
import pdb

from django.contrib.auth import get_user_model
from .serializer import ShelterSerializer, SeekerSerializer, UserSerializer, LoginSerializer
from api.models import BaseUser, PetSeeker, PetShelter, Application, Notification

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

class loginUser(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = get_user_model().objects.filter(email=email).first()

        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            data = {
                'refresh_token': str(refresh),
                'access_token': access_token,
                'user_id': user.id,
                'is_shelter': user.is_pet_shelter()
            }
            return Response(data)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
        
class StandardResultsSetPagination(PageNumberPagination):  # thanks Yahya
    page_size = 4

class AllShelterListView(generics.ListAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

class SeekerProfileView (generics.RetrieveDestroyAPIView):
    queryset = PetSeeker.objects.all()
    serializer_class = SeekerSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    
    def get_object(self):
        seeker = super().get_object()
        user = self.request.user

        if user.pk == seeker.pk:
            return seeker

        if hasattr(user, 'petshelter') and \
           Application.objects.filter(seeker=seeker, status='Pending', pet__shelter=user).exists():
            return seeker

        self.permission_denied(
            self.request,
            message="You do not have permission to view this profile."
        )

    def retrieve(self, request, *args, **kwargs):
        seeker = self.get_object()
        serializer = self.get_serializer(seeker)
        return Response(serializer.data)

class ShelterProfileView(generics.RetrieveDestroyAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        shelter = self.get_object()
        serializer = self.get_serializer(shelter)
        return Response(serializer.data)

class PetShelterUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.id != obj.id:
            self.permission_denied(self.request)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PetSeekerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PetSeeker.objects.all()
    serializer_class = SeekerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.id != obj.id:
            self.permission_denied(self.request)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)