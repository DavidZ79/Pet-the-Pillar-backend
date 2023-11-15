from rest_framework.serializers import ModelSerializer, RelatedField

from api.models import Notification, Pet, Application, Review
from api.serializer import UserRelatedField

class NotificationForwardRelatedField(RelatedField):
    queryset = Notification.objects.all()
    
    def to_representation(self, value):
        # TODO: yikes
        # if isinstance(value, PetShelter):
        #     return 'Seeker: ' + value.id
        # elif isinstance(value, PetSeeker):
        #     return 'Shelter: ' + value.id
        try:
            user = Pet.objects.get(pk=value.id)
            return 'Seeker: ' + value.id
        except Application.DoesNotExist:
            try:
                user = Application.objects.get(pk=value.id)
                return 'Shelter: ' + value.id
            except Application.DoesNotExist:
                raise Exception('Unexpected user type')
                # raise Http404('Unknown Type of user')

class NotificationSerializer(ModelSerializer):
    user = UserRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'status', 'forward', 'content']
        extra_kwargs = {'timestamp': {'read_only': True}}
    
    def create(self, validated_data):
        return Notification.objects.create(**validated_data)
    