from rest_framework import serializers
import sys
# sys.path.append("..api.models") 
# from ..api.models import newUser, PetSeeker, PetShelter
from .testmodel import newUser, PetSeeker, PetShelter

class UserSerializer (serializers.ModelSerializer):
   class Meta:
      model = newUser
      fields = ['id', 'email', 'name', 'phoneNumber', 'location', 'picture']

class PetShelterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = PetShelter
        fields = UserSerializer.Meta.fields + ['missionStatement', 'rating']

class PetSeekerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = PetSeeker
        fields = UserSerializer.Meta.fields + ['preference']
   
