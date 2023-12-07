from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

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
        
        blog = serializer.save(shelter=shelter)

class BlogAPI(RetrieveAPIView):
    serializer_class = BlogSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'shelter_id'

    def retrieve(self, request,**kwargs):
        shelter_id = self.kwargs.get('shelter_id')

        try:
            shelter = PetShelter.objects.get(pk=shelter_id)
        except PetShelter.DoesNotExist:
            raise NotFound('Application not found.')

        shelter = get_object_or_404(PetShelter, pk=self.kwargs['shelter_id'])
        blog = get_object_or_404(Blog, shelter=shelter)
        result = self.serializer_class(instance=blog)
        return JsonResponse(result.data)

class BlogListAPI(ListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        shelter_id = self.kwargs.get('shelter_id')
        
        try:
            shelter = PetShelter.objects.get(pk=shelter_id)
        except PetShelter.DoesNotExist:
            raise NotFound('Application not found.')
        
        return Blog.objects.filter(shelter=shelter)