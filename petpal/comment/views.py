from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.contenttypes.models import ContentType

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializer import ChatSerializer, ReviewSerializer

from api.models import BaseUser, PetSeeker, PetShelter, Application, Chat, Review

from datetime import datetime
# Create your views here.

class ChatAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        # print("REQUEST: ", self.request.user)
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        
        try:
            application = Application.objects.get(pk=self.kwargs['application_id'])
        except Application.DoesNotExist:
            raise Http404('Invalid Access')
        # print("email?:" + str(self.request.user))
        # print("user id:" + str(user.id))
        # print("application:" + str(application.id))
        # print("Seeker:" + str(application.seeker.id))
        # print("shelter:" + str(application.pet.shelter.id))
        print(self.get_serializer_context())        
        if application.seeker.id != user.id and application.pet.shelter.id != user.id:
            raise Http404('Invalid Access')

        chat = serializer.save(user=user, application=application)
        # print(chat.user_content_type)
        # print(ContentType.objects.get_for_model(chat.user))
        application.last_updated = datetime.now

class ReviewAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):       
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown Type of user')
        # print(self.kwargs['shelter_id'])
        # print(user.id)
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        review = serializer.save(user=user, shelter=shelter)

class ChatListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        
        
        application = get_object_or_404(Application, pk=self.kwargs['application_id'])

        if application.seeker.id != user.id and application.pet.shelter.id != user.id:
            raise Http404('Invalid Access')
        
        return Chat.objects.filter(application=application)

class ReviewListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        return Review.objects.filter(shelter=shelter)