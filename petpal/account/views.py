from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from django.views.generic.edit import View
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

from django.contrib.auth import get_user_model
from .serializer import ShelterSerializer, SeekerSerializer, UserSerializer, LoginSerializer
from api.models import BaseUser, PetSeeker, PetShelter, Application

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

        # Use Django's authenticate function for security
        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            data = {
                'refresh_token': str(refresh),
                'access_token': access_token,
                'user_id': user.id
            }
            return Response(data)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

class AllShelterListView(generics.ListAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.AllowAny]

class SeekerProfileView (generics.RetrieveAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.IsAuthenticated]  
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        seeker = self.get_object()
        shelter_id = self.kwargs.get('id')

        # Check if the shelter has an active application with the seeker
        active_application_exists = Application.objects.filter(seeker=seeker, status='Pending', pk=shelter_id).exists()

        if active_application_exists:
            serializer = self.get_serializer(seeker)
            return Response(serializer.data)
        else:
            return Response({'error': 'Shelter does not have an active application with this seeker.'}, status=403)

class ShelterProfileView(generics.RetrieveAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        shelter = self.get_object()

        if not self.request.user.is_authenticated:
            serializer = self.get_serializer(shelter)
            return Response(serializer.data)

        user = self.request.user

        if isinstance(user, PetShelter) and user == shelter:
            serializer = self.get_serializer(shelter)
            return Response(serializer.data)

        if isinstance(user, PetSeeker):
            application_exists = Application.objects.filter(seeker=user, status='Accepted', pet__shelter=shelter).exists()

            if application_exists:
                serializer = self.get_serializer(shelter)
                return Response(serializer.data)
            else:
                return Response({'error': 'You do not have an active application with this shelter.'}, status=403)

        return Response({'error': 'Access denied.'}, status=403)

class TestView(View):
    def get(self, request):

        d = {"id": '1', "username": '2'}
        return JsonResponse(d)
