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
from django.contrib.contenttypes.models import ContentType

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
                'user_id': user.id
            }
            return Response(data)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

class AllShelterListView(generics.ListAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.AllowAny]

class SeekerProfileView (generics.RetrieveDestroyAPIView):
    queryset = PetSeeker.objects.all()
    serializer_class = SeekerSerializer
    # permission_classes = [permissions.AllowAny]  
    permission_classes = [permissions.IsAuthenticated]  
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        seeker = self.get_object()
        shelter_id = self.kwargs.get('id')

        active_application_exists = Application.objects.filter(seeker=seeker, status='Pending', pk=shelter_id).exists()

        if active_application_exists:
            serializer = self.get_serializer(seeker)
            return Response(serializer.data)
        else:
            return Response({'error': 'Shelter does not have an active application with this seeker.'}, status=403)
    
    def destroyApp(self, request, *args, **kwargs):
        seeker = self.get_object()
        shelter_id = self.kwargs.get('id')

        applications = Application.objects.filter(seeker=seeker, pet__shelter_id=shelter_id)
        applications.delete()

        return Response({'message': 'All applications for the seeker have been deleted.'})

    def destroyNoti(self, request, *args, **kwargs):
        seeker = self.get_object()

        notifications = Notification.objects.filter(user_content_type=ContentType.objects.get_for_model(seeker), user_object_id=seeker.id)
        notifications.delete()

        return Response({'message': 'Notification deleted successfully.'})

class ShelterProfileView(generics.RetrieveDestroyAPIView):
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
            application_exists = Application.objects.filter(seeker=user, status='Pending', pet__shelter=shelter).exists()

            if application_exists:
                serializer = self.get_serializer(shelter)
                return Response(serializer.data)
            else:
                return Response({'error': 'You do not have an active application with this shelter.'}, status=403)

        return Response({'error': 'Access denied.'}, status=403)
    
    def destroyListing (self, request, *args, **kwargs):
        pass

    def destroyNoti(self, request, *args, **kwargs):
        shelter = self.get_object()

        notifications = Notification.objects.filter(user_content_type=ContentType.objects.get_for_model(shelter), user_object_id=shelter.id)
        notifications.delete()

        return Response({'message': 'Notification deleted successfully.'})

class PetShelterUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PetShelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [permissions.IsAuthenticated]

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class TestView(View):
    def get(self, request):

        d = {"id": '1', "username": '2'}
        return JsonResponse(d)
