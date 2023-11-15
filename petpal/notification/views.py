from django.shortcuts import render, get_object_or_404
from django.http import Http404

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.models import Notification, PetSeeker, PetShelter

from .serializer import NotificationSerializer
# Create your views here.

class NotificationCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = [NotificationSerializer]
    
    def perform_create(self, serializer):
        notification = serializer.save()
        

class NotificationAPI(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = [NotificationSerializer]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.status = 'Read'
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

class NotificationListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user = PetSeeker.objects.get(pk=self.kwargs[self.request.user.id])
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.kwargs[self.request.user.id])
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')

        return Notification.objects.filter(user=user)
