from rest_framework.serializers import ModelSerializer

from api.models import Comment, Chat, Review
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
            # 'user_object_id': {'read_only': True}, 
            'application': {'required':False}
            }

    def create(self, validated_data):
        # print(validated_data)
        return Chat.objects.create(**validated_data)

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