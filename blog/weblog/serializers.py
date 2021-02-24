from rest_framework import serializers
from .models import Category ,Comment, LikePost, LikeComment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')
        
        
class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    value = serializers.BooleanField()
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text','post')

# class CommentSerializer(serializers.Serializer):
#     text = serializers.CharField()
#     post_id = serializers.IntegerField()

class LikePostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LikePost
        fields = ('id','value','user','post')

class LikeCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LikeComment
        fields = ('id','value','user','comment')