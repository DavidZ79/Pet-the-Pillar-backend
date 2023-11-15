from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse

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
        

class NotificationAPI(RetrieveAPIView, DestroyAPIView):
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

    def retrieve(self, request,**kwargs):
        print(request.__dict__.keys())
        print(kwargs)
        try:
            notification =  Notification.objects.get(pk=kwargs['notification_id'])
        except Notification.DoesNotExist:
            raise Http404('Bad notification Id')
        # result = self.serializer_class
        result = self.serializer_class(instance=notification)
        notification.status = "Read" #Update notification
        notification.save()
        return JsonResponse(result.data)
    
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
        status = self.request.query_params.get('status')
        if status:
            if status not in ['Unread', 'Read']:
                raise Http404('Bad Notification Status')
            else:
                return user.notifications.all().filter(status=status)
        else:
            return user.notifications.all()