from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from api.models import BaseUser, PetSeeker, PetShelter

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id', 'username', 'email', 'password', 'phoneNumber', 'location', 'picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = BaseUser.objects.create_user(**validated_data)
        return user

    def validate_password(self, value):
        validate_password(value)
        return value

class LoginSerializer (serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'password']
    
class ShelterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = PetShelter
        fields = UserSerializer.Meta.fields + ['missionStatement', 'totalRating', 'numberOfRating']
    
    def create(self, validated_data):
        user = PetShelter.objects.create_user(**validated_data)
        return user
        
class SeekerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = PetSeeker
        fields = UserSerializer.Meta.fields + ['preference']

    def create(self, validated_data):
        user = PetSeeker.objects.create_user(**validated_data)
        return user
