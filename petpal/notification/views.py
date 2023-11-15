from django.shortcuts import render, get_object_or_404
from django.http import Http404

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.models import Notification, PetSeeker, PetShelter, Pet, Application, Review

from .serializer import NotificationSerializer
# Create your views here.

class NotificationCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def perform_create(self, serializer):
        print("GOT TO CREATE")
        print(self.request.data)
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        
        try:
            forward = Pet.objects.get(pk=self.request.data['forward'])
        except Pet.DoesNotExist:
            try:
                forward = Application.objects.get(pk=self.request.user)
            except Application.DoesNotExist:
                raise Http404('Unknown User')
        
        notification = serializer.save(user=user, forward=forward)
        

class NotificationAPI(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'notification_id'

    def get_queryset(self):
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        return user.notifications.all()

    def retrieve(self, request, *args, **kwargs):
        print(request.__dict__)
        # return self.get()
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        print("UPDATE")
        print(serializer)
        serializer.status = 'Read'
        serializer.save()
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

class NotificationListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'notification_id'

    def get_queryset(self):
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        return user.notifications.all()