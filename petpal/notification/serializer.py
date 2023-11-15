from rest_framework.serializers import ModelSerializer, RelatedField, HyperlinkedRelatedField, ValidationError
from django.http import Http404
from rest_framework.reverse import reverse

from api.models import Notification, Pet, Application, Review, Chat
from api.serializers import UserRelatedField

from pet.views import ManagePetView

class NotificationForwardRelatedField(HyperlinkedRelatedField):
    queryset = Notification.objects.all() # XD?
    view_name = "forward"
    
    def to_representation(self, value):
        print("REPRESENTING")
        print(self.context)
        if isinstance(value, Pet):
            return f'PetId({value.id})'
            # return reverse('create-pet', request=self.context['request'])
            # return reverse('notification_list', kwargs={'pk':value.id})
        elif isinstance(value, Application):
            return f'ApplicationId({value.id})'
        elif isinstance(value, Review):
            return f'ReviewID({value.id})'
        elif isinstance(value, Chat):
            return f'ChatID({value.id})'
        # try:
        #     user = Pet.objects.get(pk=value.id)
        #     return 'Seeker: ' + value.id
        # except Application.DoesNotExist:
        #     try:
        #         user = Application.objects.get(pk=value.id)
        #         return 'Shelter: ' + value.id
        #     except Application.DoesNotExist:
        #         raise Exception('Unexpected user type')
        raise Http404('Unknown object')
    
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
            'status': {'required': False},
            }
    
    def create(self, validated_data):
        return Notification.objects.create(**validated_data)
    