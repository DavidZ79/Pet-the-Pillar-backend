from rest_framework.serializers import ModelSerializer, RelatedField, ValidationError
from django.http import Http404

from api.models import Notification, Pet, Application, Review
from api.serializers import UserRelatedField

class NotificationForwardRelatedField(RelatedField):
    queryset = Notification.objects.all() # XD?
    
    def to_representation(self, value):
        print("REPRESENTING")
        if isinstance(value, Pet):
            return f'PetId:({value.id})'
        elif isinstance(value, Application):
            return f'ApplicationId:({value.id})'
        elif isinstance(value, Review):
            return f'ReviewID:({value.id})'
        # try:
        #     user = Pet.objects.get(pk=value.id)
        #     return 'Seeker: ' + value.id
        # except Application.DoesNotExist:
        #     try:
        #         user = Application.objects.get(pk=value.id)
        #         return 'Shelter: ' + value.id
        #     except Application.DoesNotExist:
        #         raise Exception('Unexpected user type')
        raise Http404('Unknown Type of user')
    
    def to_internal_value(self, data):
        print("VALIDATING?")
        try:
            try:
                print(data)
                id = data
                try:
                    user = Pet.objects.get(pk=id)
                except Pet.DoesNotExist:
                    try:
                        user = Review.objects.get(pk=id)
                    except Review.DoesNotExist:
                        raise ValidationError(
                            'Obj does not exist.'
                        )
                return Pet.objects.get(pk=id)
            except KeyError:
                raise ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise ValidationError(
                    'id must be an integer.'
                )
        except Pet.DoesNotExist:
            raise ValidationError(
                'User does not exist.'
            )

class NotificationSerializer(ModelSerializer):
    user = UserRelatedField()
    forward = NotificationForwardRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'status', 'forward', 'content', 'timestamp']
        extra_kwargs = {
            'timestamp': {'read_only': True},
            'status': {'read_only': True},
            }
    
    def create(self, validated_data):
        return Notification.objects.create(**validated_data)
    