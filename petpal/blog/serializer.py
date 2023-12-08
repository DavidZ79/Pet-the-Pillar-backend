from rest_framework.serializers import ModelSerializer
from django.contrib.contenttypes.models import ContentType
from api.models import Blog
from api.serializers import UserRelatedField

class BlogSerializer(ModelSerializer):

    class Meta:
        model = Blog
        fields = [ 'id', 'shelter', 'content', 'title', 'num_likes', 'timestamp']
        extra_kwargs = {
            # 'user_object_id': {'read_only': True}, 
            # 'user': {'read_only': True},
            'shelter': {'required': False},
            'num_likes': {'required': False, 'read_only': True},
            'timestamp': {'read_only': True}}
    
    def create(self, validated_data):
        # Get the content type for the user model
        user_content_type = ContentType.objects.get_for_model(self.context['request'].user)

        # Create the blog instance
        # blog = Blog.objects.create(
        #     content=validated_data['content'],
        #     title=validated_data['title'],
        #     # shelter=self.context['request'].user,
        #     shelter=validated_data['shelter'],
        # )
        return Blog.objects.create(**validated_data)