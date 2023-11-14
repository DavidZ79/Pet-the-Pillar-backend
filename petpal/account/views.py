from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .testmodel import newUser, PetShelter, PetSeeker
from .serializer import UserSerializer, PetSeekerSerializer, PetShelterSerializer
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
   if request.method == 'POST':
      serializer = UserSerializer(data=request.data)

      if serializer.is_valid():
         user = serializer.save()

         refresh = RefreshToken.for_user(user)
         data = {
               'refresh': str(refresh),
               'access': str(refresh.access_token),
         }
         return Response(data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def registerShelter(request):
   if request.method == 'POST':
        serializer = PetShelterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['POST'])
@permission_classes([AllowAny])
def registerSeeker(request):
    if request.method == 'POST':
        serializer = PetSeekerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
