from rest_framework.serializers import ModelSerializer
from django.contrib.contenttypes.models import ContentType
from api.models import Comment, Chat, Review, Discussion, Ratings, Likes
from api.serializers import UserRelatedField, RelatedField

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
        fields = CommentSerializer.Meta.fields + ['shelter', 'parent', 'review_children']
        extra_kwargs = {
            # 'user_object_id': {'read_only': True}, 
            'shelter': {'required':False},
            'parent': {'required':False},
            'review_children': {'read_only':True},
            }
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)
    
class DiscussionSerializer(CommentSerializer):
    class Meta():
        model = Discussion
        fields = CommentSerializer.Meta.fields + ['blog', 'parent', 'discussion_children']
        extra_kwargs = {
            # 'user_object_id': {'read_only': True}, 
            'blog': {'required':False},
            'parent': {'required':False},
            'discussion_children': {'read_only':True},
            }
    
    def create(self, validated_data):
        return Discussion.objects.create(**validated_data)

class RatingsSerializer(ModelSerializer):
    user = UserRelatedField()
    partial = True

    class Meta():
        model = Ratings
        fields = ['id', 'shelter', 'user', 'rating']
        extra_kwargs = {
            'shelter': {'required': False},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        # Get the content type for the user model
        user_content_type = ContentType.objects.get_for_model(self.context['request'].user)

        # Create the rating instance
        rating = Ratings.objects.create(
            shelter = validated_data['shelter'],
            rating = validated_data['rating'],
            user_content_type=user_content_type,
            user_object_id=self.context['request'].user.pk,
        )

        return rating
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

class LikesSerializer(ModelSerializer):
    user = UserRelatedField()

    class Meta():
        model = Likes
        fields = ['blog', 'user']
        extra_kwargs = {
            'blog': {'required': False}
        }
    
    def create(self, validated_data):
        # Get the content type for the user model
        user_content_type = ContentType.objects.get_for_model(self.context['request'].user)

        # Create the rating instance
        likes = Likes.objects.create(
            blog = validated_data['blog'],
            user_content_type=user_content_type,
            user_object_id=self.context['request'].user.pk,
        )

        return likes
