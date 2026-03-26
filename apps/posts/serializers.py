from rest_framework import serializers
from .models import Post , Comment
from apps.users.serializers import UserSerializer

# main post serializer responsible for showing/updating posts
class PostSerializer(serializers.ModelSerializer):
    # we already have author_id but we need author object 
    author = UserSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    # determines if current user liked this post or not
    is_liked = serializers.SerializerMethodField()

    # determine if the current user is the owner of the post or not
    is_owner = serializers.SerializerMethodField()

    def get_is_liked(self , obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # check whether if they are any like made by our user to this post
            return obj.likes.filter(user=request.user).exists()
        
        return False
    
    def get_is_owner(self , obj):
        request = self.context.get('request')
        return request.user == obj.author


    class Meta:
        model = Post
        fields = ('id','author','content','image','likes_count','comments_count' , 'is_liked' , 'is_owner')
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

