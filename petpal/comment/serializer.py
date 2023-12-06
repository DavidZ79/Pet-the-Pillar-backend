from rest_framework.serializers import ModelSerializer
from django.contrib.contenttypes.models import ContentType
from api.models import Comment, Chat, Review, Discussion
from api.serializers import UserRelatedField

class CommentSerializer(ModelSerializer):
    user = UserRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'timestamp']
        extra_kwargs = {
            # 'user_object_id': {'read_only': True}, 
            # 'user': {'read_only': True},
            'timestamp': {'read_only': True}}
        
class ChatSerializer(CommentSerializer):
    class Meta():
        model = Chat
        fields = CommentSerializer.Meta.fields + ['application']
        # extra_kwargs = CommentSerializer.Meta.extra_kwargs.update({'application':{'required':False}})
        # extra_kwargs = {'application':{'required':False}}.update(CommentSerializer.Meta.extra_kwargs)
        # extra_kwargs = CommentSerializer.Meta.extra_kwargs + {'application': {}}
        extra_kwargs = {
            'user': {'read_only': True}, 
            'application': {'required':False}
            }

    def create(self, validated_data):
        # Get the content type for the user model
        user_content_type = ContentType.objects.get_for_model(self.context['request'].user)

        # Create the chat instance
        chat = Chat.objects.create(
            content=validated_data['content'],
            user_content_type=user_content_type,
            user_object_id=self.context['request'].user.pk,
            application=validated_data['application']
        )

        return chat

class ReviewSerializer(CommentSerializer):
    class Meta():
        model = Review
        fields = CommentSerializer.Meta.fields + ['shelter', 'rating']
        extra_kwargs = {
            # 'user_object_id': {'read_only': True}, 
            'shelter': {'required':False}
            }
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)
    
class DiscussionSerializer(CommentSerializer):
    class Meta():
        model = Discussion
        fields = CommentSerializer.Meta.fields + ['blog']
        extra_kwargs = {
            # 'user_object_id': {'read_only': True}, 
            # 'shelter': {'required':False}
            }
    
    def create(self, validated_data):
        return Discussion.objects.create(**validated_data)