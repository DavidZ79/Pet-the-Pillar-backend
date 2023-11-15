from rest_framework import status
from rest_framework.response import Response
from api.models import Application, Pet, PetShelter, PetSeeker
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import ApplicationSerializer


class ApplicationCreateView(APIView):

    def post(self, request):  # Create

        # create application
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, application_id):  # Update

        def isShelterOrSeeker(user):  # helper function
            if isinstance(user, PetShelter):
                return 'shelter'
            elif isinstance(user, PetSeeker):
                return 'seeker'
            else:
                print("error: not shelter or seeker")
                return 'error'

        application = Application.objects.get(pk=application_id)
        new_status = request.data.get('status')

        user = request.user
        # user is a shelter
        if isShelterOrSeeker(user) == 'shelter':
            if application.status == 'pending' and new_status in ['Accepted', 'Denied']:
                application.status = new_status
            else:
                return Response({'error': 'Invalid status update'}, status=status.HTTP_400_BAD_REQUEST)
        # user is a seeker
        elif isShelterOrSeeker(user) == 'seeker':
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
    permission_classes = [IsAuthenticated]
    #filter_backends = [DjangoFilterBackend, OrderingFilter] causes crash
    filterset_fields = ['status']
    ordering_fields = ['timestamp', 'last_updated']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, PetShelter):
            return Application.objects.filter(pet__shelter=user)
        else:
            # return an empty queryset
            return Application.objects.none()


class StandardResultsSetPagination(PageNumberPagination):  # thanks Yahya
    page_size = 10
