from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from api.models import Application, Pet, BaseUser
from rest_framework.views import APIView
from .serializers import ApplicationSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class ApplicationCreateView(APIView):

    def post(self, request):  
        pet_id = request.data.get('pet')
        pet = get_object_or_404(Pet, id=pet_id)

        if pet.status != 'Available':
            return Response({'error': 'Pet is not available'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not BaseUser.is_pet_seeker(request.user):
            return Response(
                {"error": "You are not authorized to create a pet application."},
                status=status.HTTP_403_FORBIDDEN)
        
        request.data['status'] = 'Pending'        
        request.data['seeker'] = request.user.petseeker.pk
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, application_id):  # Update
        application = Application.objects.get(pk=application_id)
        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {"error": "No new status provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if hasattr(request.user, 'petseeker') and request.user.petseeker == application.seeker:
            if application.status in ['Pending', 'Accepted'] and new_status == 'Withdrawn':
                application.status = new_status
                application.save(update_fields=['status'])
                return Response({"status": new_status}, status=status.HTTP_200_OK)

        elif hasattr(request.user, 'petshelter') and request.user.petshelter == application.pet.shelter:
            if application.status == 'Pending' and new_status in ['Accepted', 'Denied']:
                application.status = new_status
                application.save(update_fields=['status'])
                return Response({"status": new_status}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid status update request."},
            status=status.HTTP_400_BAD_REQUEST
        )


class ApplicationListView(ListAPIView):
    serializer_class = ApplicationSerializer
    filterset_fields = ['status']
    ordering_fields = ['timestamp', 'last_updated']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.all()

        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)

        ordering = self.request.query_params.get('ordering')
        if ordering is not None:
            queryset = queryset.order_by(ordering)

        if hasattr(user, 'petshelter'):
            return Application.objects.filter(pet__shelter=user.petshelter)
        elif hasattr(user, 'petseeker'):
            return Application.objects.filter(seeker=user.petseeker)
        else:
            return Application.objects.none()

class StandardResultsSetPagination(PageNumberPagination):  # thanks Yahya
    page_size = 10
