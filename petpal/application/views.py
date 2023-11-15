from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from api.models import Application, PetShelter, Pet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import ApplicationSerializer


class ApplicationCreateView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        pet_id = self.request.data.get('pet')
        pet = get_object_or_404(Pet, id=pet_id)
        if pet.status != 'Available':
            raise serializer.ValidationError('This pet is not available for adoption.')
        serializer.save(seeker=self.request.user)


class ApplicationView(RetrieveAPIView, UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        application = self.get_object()
        user = self.request.user
        serializer.save()


class ApplicationListView(ListAPIView):
    serializer_class = ApplicationSerializer
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter] causes crashes
    filterset_fields = ['status']
    ordering_fields = ['timestamp', 'last_updated']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'petshelter'):
            return Application.objects.filter(pet__shelter=user.petshelter)
        elif hasattr(user, 'petseeker'):
            return Application.objects.filter(seeker=user.petseeker)
        else:
            # user is not seeker or shelter
            print("Error: user is not seeker or shelter")
            return Application.objects.none()


class StandardResultsSetPagination(PageNumberPagination):  # thanks Yahya
    page_size = 10
