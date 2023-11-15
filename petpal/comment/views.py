from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.contenttypes.models import ContentType

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

from .serializer import ChatSerializer, ReviewSerializer

from api.models import BaseUser, PetSeeker, PetShelter, Application, Chat, Review, Notification

from datetime import datetime
# Create your views here.

class ChatAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')

        application_id = self.kwargs.get('application_id')
        try:
            application = Application.objects.get(pk=application_id)
        except Application.DoesNotExist:
            raise NotFound('Application not found.')

        if application.seeker.id != user.id and application.pet.shelter.id != user.id:
            raise PermissionDenied('Invalid Access')

        chat = serializer.save(user=user, application=application)
        application.last_updated = datetime.now

        notification_content = f"New chat message in application {application_id}"
        receiver = application.pet.shelter if hasattr(user, 'petseeker') else application.seeker.user

        Notification.objects.create(
            user_content_type=ContentType.objects.get_for_model(receiver),
            user_object_id=receiver.id,
            content=notification_content,
            forward_content_type=ContentType.objects.get_for_model(chat),
            forward_object_id=chat.id
        )

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

        notification_content = f"A new review has been posted by {user.username}."
        Notification.objects.create(
            user_content_type=ContentType.objects.get_for_model(shelter),
            user_object_id=shelter.id,
            content=notification_content,
            forward_content_type=ContentType.objects.get_for_model(review),
            forward_object_id=review.id
        )

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
        
        
        application_id = self.kwargs.get('application_id')
        try:
            application = Application.objects.get(pk=application_id)
        except Application.DoesNotExist:
            raise NotFound('Application not found.')

        if application.seeker.id != user.id and application.pet.shelter.id != user.id:
            raise PermissionDenied('Invalid Access')

        if application.seeker.id != user.id and application.pet.shelter.id != user.id:
            raise Http404('Invalid Access')
        
        return Chat.objects.filter(application=application)

class ReviewListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        return Review.objects.filter(shelter=shelter)