from django.shortcuts import render, get_object_or_404
from django.http import Http404

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializer import ChatSerializer, ReviewSerializer

from api.models import BaseUser, PetSeeker, PetShelter, Application, Chat, Review
# Create your views here.

class ChatAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        try:
            user = PetSeeker.objects.get(pk=self.kwargs[self.request.user.id])
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.kwargs[self.request.user.id])
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        
        application = get_object_or_404(Application, pk=self.kwargs['application_id'])
        
        if application.seeker.id != user.id and application.pet.shelter.id != user.id:
            raise Http404('Invalid Access')

        chat = serializer.save(application=application)

class ReviewAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):       
        try:
            user = PetSeeker.objects.get(pk=self.kwargs[self.request.user.id])
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.kwargs[self.request.user.id])
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown Type of user')
        
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        review = serializer.save(user=user, shelter=shelter)

class ChatListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user = PetSeeker.objects.get(pk=self.kwargs[self.request.user.id])
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.kwargs[self.request.user.id])
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        

        application = get_object_or_404(Application, pk=self.kwargs['application_id'])
        return Chat.objects.filter(application=application)

class ReviewListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        return Review.objects.filter(shelter=shelter)