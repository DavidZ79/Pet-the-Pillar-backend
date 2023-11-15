from rest_framework.serializers import RelatedField, ValidationError
from django.http import Http404

from .models import BaseUser, PetSeeker, PetShelter

class UserRelatedField(RelatedField):
    queryset = BaseUser.objects.all()
    
    def to_internal_value(self, data):
        try:
            try:
                id = data
                try:
                    user = PetSeeker.objects.get(pk=id)
                except PetSeeker.DoesNotExist:
                    try:
                        user = PetShelter.objects.get(pk=id)
                    except PetShelter.DoesNotExist:
                        raise ValidationError(
                            'Obj does not exist.'
                        )
                return BaseUser.objects.get(pk=id)
            except KeyError:
                raise ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise ValidationError(
                    'id must be an integer.'
                )
        except BaseUser.DoesNotExist:
            raise ValidationError(
                'User does not exist.'
            )
    
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