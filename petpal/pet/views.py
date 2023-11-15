from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework import status, generics
from api.models import Pet
from .serializers import PetSerializer
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class ManagePetView(APIView):
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    
class SearchPetView(generics.ListAPIView):
    serializer_class = PetSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering = ["name"]
    ordering_fields = ['name', 'age', 'size', 'species', 'status']

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
        if min_age and max_age:
            queryset = queryset.filter(age__gte=min_age, age__lte=max_age)

        return queryset
    