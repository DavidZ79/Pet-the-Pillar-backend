from rest_framework.serializers import ModelSerializer, RelatedField

from api.models import Comment, Chat, Review
from api.serializers import UserRelatedField



class CommentSerializer(ModelSerializer):
    user = UserRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'timestamp', 'user']
        
class ChatSerializer(CommentSerializer):
    class Meta():
        model = Chat
        fields = CommentSerializer.Meta.fields + ['application']
    
    def create(self, validated_data):
        return Chat.objects.create(**validated_data)

class ReviewSerializer(CommentSerializer):
    class Meta():
        model = Review
        fields = CommentSerializer.Meta.fields + ['shelter', 'rating']
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)