from rest_framework import serializers
from .models import Post , Comment
from apps.users.serializers import UserSerializer

# main post serializer responsible for showing/updating posts
class PostSerializer(serializers.ModelSerializer):
    # we already have author_id but we need author object 
    author = UserSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id','author','content','image','likes_count','comments_count')
        read_only_fields = ('id','author','created_at')



# post serializer for creating new posts
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id' , 'content' , 'image')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id',  'author' , 'content' , 'created_at')
        read_only_fields = ('id' , 'author' , 'created_at')

