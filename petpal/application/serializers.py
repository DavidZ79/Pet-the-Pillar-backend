from rest_framework import serializers
from APPNAMEHERE.models import Item  # TODO import model

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item  # TODO replace with model
        fields = '__all__'