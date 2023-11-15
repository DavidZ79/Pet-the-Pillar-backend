from rest_framework.serializers import RelatedField
from django.http import Http404

from .models import BaseUser, PetSeeker, PetShelter

class UserRelatedField(RelatedField):
    queryset = BaseUser.objects.all()
    def to_representation(self, value):
        # if isinstance(value, PetShelter):
        #     return 'Seeker: ' + value.id
        # elif isinstance(value, PetSeeker):
        #     return 'Shelter: ' + value.id
        try:
            user = PetSeeker.objects.get(pk=value.id)
            return 'Seeker: ' + value.id
        except PetSeeker.DoesNotExist:
            try:
                user = PetShelter.objects.get(pk=value.id)
                return 'Shelter: ' + value.id
            except PetSeeker.DoesNotExist:
                raise Exception('Unexpected user type')
                # raise Http404('Unknown Type of user')