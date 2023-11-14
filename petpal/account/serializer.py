from rest_framework import serializers
from api.models import BaseUser, PetSeeker, PetShelter

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id', 'email', 'password', 'name', 'phoneNumber', 'location']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = BaseUser.objects.create_user(**validated_data)
        return user
    
class ShelterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = PetShelter
        fields = '__all__'
        

class SeekerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = PetSeeker
        fields = '__all__'
