from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from rest_framework.response import Response

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from .serializer import BlogSerializer

from api.models import Blog, PetShelter

class BlogCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        try:
            shelter = PetShelter.objects.get(pk=self.request.user)
        except PetShelter.DoesNotExist:
            raise NotFound('Unknown Shelter')
        print(shelter)
        blog = serializer.save(shelter=shelter)

class BlogAPI(RetrieveAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'blog_id'

    def retrieve(self, request,**kwargs):
        blog_id = self.kwargs.get('blog_id')

        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            raise NotFound('Blog not found.')

        result = self.serializer_class(instance=blog)
        return JsonResponse(result.data)
    
    def patch(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.num_likes += 1  # Increment the likes
        blog.save()
        return Response(self.get_serializer(blog).data)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
class BlogListAPI(ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        shelter_id = self.kwargs.get('shelter_id')
        
        try:
            shelter = PetShelter.objects.get(pk=shelter_id)
        except PetShelter.DoesNotExist:
            raise NotFound('Shelter not found.')
        
        return Blog.objects.filter(shelter=shelter)
    

class BlogListAPI2(ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        shelter_id = self.kwargs.get('shelter_id')
        
        try:
            shelter = PetShelter.objects.get(pk=shelter_id)
        except PetShelter.DoesNotExist:
            raise NotFound('Shelter not found.')
        
        return Blog.objects.filter(shelter=shelter)