from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib.contenttypes.models import ContentType

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

from .serializer import ChatSerializer, ReviewSerializer, DiscussionSerializer, RatingsSerializer, LikesSerializer

from api.models import BaseUser, PetSeeker, PetShelter, Application, Blog, Chat, Review, Notification, Ratings, Likes


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
        application.last_updated = datetime.now()
        application.save()

        notification_content = f"New chat message in application {application_id}"
        receiver = application.pet.shelter if hasattr(user, 'petseeker') else application.seeker

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

class DiscussionAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DiscussionSerializer

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
        blog = get_object_or_404(Blog, pk=self.kwargs['blog_id'])
        discussion = serializer.save(user=user, blog=blog)

        notification_content = f"A new discusion has been posted by {user.username} on \"{blog.title}\"."
        Notification.objects.create(
            user_content_type=ContentType.objects.get_for_model(blog.shelter),
            user_object_id=blog.shelter.id,
            content=notification_content,
            forward_content_type=ContentType.objects.get_for_model(discussion),
            forward_object_id=discussion.id
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
    serializer_class = ReviewSerializer

    def get_queryset(self):
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        return Review.objects.filter(shelter=shelter)

class DiscussionListAPI(ListAPIView):
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        return Review.objects.filter(shelter=shelter)

class RatingAPI(CreateAPIView, RetrieveAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingsSerializer
    lookup_field = 'shelter'
    lookup_url_kwarg = 'shelter_id'

    def get_queryset(self):
        return Ratings.objects.filter(user_object_id = self.request.user.id)

    def perform_create(self, serializer, **kwargs):
        print("getting here")
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown Type of user')

        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        
        found = Ratings.objects.filter(user_object_id=user.id, shelter=shelter)
            
        if found:
            raise PermissionDenied("Rating already exists")
        
        rating = serializer.save(user=user, shelter=shelter)
        print(rating)
        shelter.numberOfRating += 1
        shelter.totalRating += rating.rating
        shelter.save()
    
    def retrieve(self, request,**kwargs):
        print(request.__dict__.keys())
        print(kwargs)
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown Type of user')

        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        
        found = Ratings.objects.filter(user_object_id=user.id, shelter=shelter)
        print(found)
        print(Ratings.objects.all())
        if not found:
            raise PermissionDenied("Rating does not exist")
        result = self.serializer_class(instance=found[0])
        return JsonResponse(result.data)

    def patch(self, request, **kwargs):
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown Type of user')
        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        found = Ratings.objects.filter(user_object_id=user.id, shelter=shelter)
        print(found)
        if not found:
            raise PermissionDenied("Rating does not exist")
        rating = found[0]
        original_rating = rating.rating
        serializer = self.serializer_class(instance=rating, data=request.data, partial=True)  # set partial=True to update a data partially
        if found:
            print(found[0].rating)
        if serializer.is_valid():
            serializer.save(user=user)
            self.perform_update(serializer)
            shelter.totalRating += int(request.data['rating']) - original_rating
            shelter.save()
            return JsonResponse(data=serializer.data)
        return Http404("wrong parameters")

    # def perform_update(self, serializer):
    #     try:
    #         user = PetSeeker.objects.get(pk=self.request.user)
    #     except PetSeeker.DoesNotExist:
    #         try:
    #             user = PetShelter.objects.get(pk=self.request.user)
    #         except PetSeeker.DoesNotExist:
    #             raise Http404('Unknown Type of user')
    #     shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
    #     found = Ratings.objects.filter(user_object_id=user.id, shelter=shelter)
    #     if not found:
    #         raise PermissionDenied("Rating does not exist")
    #     rating = found[0]
    #     print(f"rating {serializer.validated_data['rating']}")
    #     print(f"rating object {rating}")
    #     original_rating = rating.rating
    #     rating = serializer.save()
    #     shelter.totalRating += rating.rating - original_rating
    #     shelter.save()
    

class LikesAPI(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    permissions_classes = [IsAuthenticated]
    serializer_class = LikesSerializer
    lookup_field = 'blog'
    lookup_url_kwarg = 'blog_id'


    def get_queryset(self):
        return Likes.objects.all()

    def perform_create(self, serializer):
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown User')
        
        blog = get_object_or_404(Blog, pk=self.kwargs['blog_id'])

        found = Likes.objects.filter(user_object_id=user.id, blog=blog)

        if found:
            raise PermissionDenied("Like already exists")
        
        likes = serializer.save(user=user, blog=blog)

    def retrieve(self, request,**kwargs):
        try:
            user = PetSeeker.objects.get(pk=self.request.user)
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=self.request.user)
            except PetSeeker.DoesNotExist:
                raise Http404('Unknown Type of user')

        blog = get_object_or_404(Blog, pk=self.kwargs['blog_id'])
        
        found = Likes.objects.filter(user_object_id=user.id, blog=blog)

        if not found:
            raise PermissionDenied("Like does not exist")
        result = self.serializer_class(instance=found[0])
        return JsonResponse(result.data)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)