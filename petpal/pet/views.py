from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from api.models import Pet, Photo, BaseUser
from .serializers import PetSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

class ManagePetView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    
    def post(self, request):
        if not BaseUser.is_pet_shelter(request.user):
            return Response(
                {"error": "You are not authorized to create a pet listing."},
                status=status.HTTP_403_FORBIDDEN)
        
        pet_data = request.data.copy()
        print(pet_data)
        pet_data.pop('shelter', None)
        pet_data.pop('timestamp', None)
        pet_data['status'] = 'Available'

        serializer = PetSerializer(data=pet_data)
        if serializer.is_valid():
            pet = serializer.save(shelter=request.user.petshelter)
            self.handle_photo_upload(request, pet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pet_id):
        if request.user.pk != Pet.objects.get(id=pet_id).shelter.pk:
            return Response(
                {"error": "You are not authorized to edit this pet listing."},
                status=status.HTTP_403_FORBIDDEN)
        pet = get_object_or_404(Pet, id=pet_id)
        pet_data = request.data.copy()
        if pet_data.get('status') == 'Withdrawn':
            pet.status = 'Withdrawn'
        pet_data.pop('shelter', None)
        pet_data.pop('timestamp', None)
        serializer = PetSerializer(pet, data=pet_data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            self.handle_photo_upload(request, pet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pet_id):
        if request.user.pk != Pet.objects.get(id=pet_id).shelter.pk:
            return Response(
                {"error": "You are not authorized to edit this pet listing."},
                status=status.HTTP_403_FORBIDDEN)
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, _, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def handle_photo_upload(self, request, pet):
        photo_files = request.FILES.getlist('photos')
        for photo_file in photo_files:
            photo = Photo.objects.create(image=photo_file)  
            pet.photos.add(photo)
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4

class ListPetView(generics.ListAPIView):
    serializer_class = PetSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return Pet.objects.filter(shelter=user)
    
class SearchPetView(generics.ListAPIView):
    serializer_class = PetSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    permission_classes = [AllowAny]
    ordering = ["timestamp"]
    ordering_fields = ['name', 'age', 'size', 'species', 'status', 'shelter__username']

    def get_queryset(self):
        
        queryset = Pet.objects.all()
        name = self.request.query_params.get('name')
        breed = self.request.query_params.get('breed')
        species = self.request.query_params.get('species')
        location = self.request.query_params.get('location')
        gender = self.request.query_params.get('gender')
        color = self.request.query_params.get('color')
        size = self.request.query_params.get('size')
        status = self.request.query_params.get('status')
        min_age = self.request.query_params.get('min_age')
        max_age = self.request.query_params.get('max_age')
        shelter_username = self.request.query_params.get('shelter_username') 

        if name:
            queryset = queryset.filter(name__icontains=name)
        if breed:
            queryset = queryset.filter(breed__icontains=breed)
        if species:
            queryset = queryset.filter(species__icontains=species)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        if color:
            queryset = queryset.filter(color__icontains=color)
        if size:
            queryset = queryset.filter(size__iexact=size)
        if status:
            queryset = queryset.filter(status__iexact=status)
        else:
            queryset = queryset.filter(status__iexact='Available')
        if min_age and max_age:
            queryset = queryset.filter(age__gte=min_age, age__lte=max_age)
        if shelter_username:
            queryset = queryset.filter(shelter__username__icontains=shelter_username) 

        return queryset
    