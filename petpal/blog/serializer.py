from rest_framework.serializers import ModelSerializer
from django.contrib.contenttypes.models import ContentType
from api.models import Blog
from api.serializers import UserRelatedField

class BlogSerializer(ModelSerializer):
    user = UserRelatedField()

    class Meta:
        model = Blog
        fields = ['shelter', 'content', 'title', 'likes', 'timestamp']
        extra_kwargs = {
            # 'user_object_id': {'read_only': True}, 
            # 'user': {'read_only': True},
            'shelter': {''},
            'likes': {'required': False},
            'timestamp': {'read_only': True}}