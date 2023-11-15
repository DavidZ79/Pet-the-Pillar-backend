from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from api.models import Application, Pet
from rest_framework.views import APIView
from .serializers import ApplicationSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class ApplicationCreateView(APIView):

    def post(self, request):  # Create

        # # see if there exists pet listings
        # pet_listing_id = request.data.get('pet_listing_id')
        # try:
        #     pet_listing = Pet.objects.get(id=pet_listing_id, status='available')
        # except Pet.DoesNotExist:
        #     return Response({'error': 'Pet listing not available'}, status=status.HTTP_400_BAD_REQUEST)

        # create application
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, application_id):  # Update
        application = Application.objects.get(pk=application_id)
        new_status = request.data.get('status')

        user = request.user
        # user is a shelter
        if self.request.user.shelter is not None:  # is user shelter?
            if application.status == 'pending' and new_status in ['Accepted', 'Denied']:
                application.status = new_status
            else:
                return Response({'error': 'Invalid status update'}, status=status.HTTP_400_BAD_REQUEST)
        # user is a seeker
        elif user.is_pet_seeker():  # TODO
            if application.status in ['pending', 'accepted'] and new_status == 'withdrawn':
                application.status = new_status
            else:
                return Response({'error': 'Invalid status update'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
