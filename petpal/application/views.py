from rest_framework.response import Response
from rest_framework.decorators import api_view
from APPNAMEHERE.models import Item  # TODO import model
from .serializers import ItemSerializer


@api_view(['GET'])
def getShelterApplicationList(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createApplication(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])  # is update different? TODO
def updateApplication(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)