from django.shortcuts import render , get_object_or_404
from rest_framework import generics , status , permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from .serializers import PostSerializer , CreatePostSerializer , CommentSerializer
from .models import Post , Like , Comment


from apps.users.models import User
from .permissions import IsOwner

# Create your views here.

# --------------------------- Feed -----------------------------------


# Feedview (get the posts of the people you're currently following)
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # get the currently logged in user
        user = self.request.user

        # get every follow object with this user as the follower
        followings = user.following.all()

        # extract those people that our user follows
        followed_users = [f.following for f in followings]

        # get the posts of those people
        posts = Post.objects.filter(author__in=followed_users)
        return posts


# DiscoverView (get all posts whether u follow them or not)
class DiscoverView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()



# --------------------------- POSTS -----------------------------------

class PostListCreateAPIView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePostSerializer
        
        return PostSerializer
   
    def get_queryset(self):
        return Post.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # adding 'author' since its not included in the CreatePostSerializer
        # and setting it to the current user
        post = serializer.save(author=self.request.user)
        return Response(PostSerializer(post , context={'request': request}).data , status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



# allows the currently logged in user to delete , edit his own post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def get_permissions(self):
        if self.request.method in ('PUT' , 'DELETE'):
            return [permissions.IsAuthenticated() , IsOwner()]


# get the posts of a specific user based on his username
class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs['username'])
        return Post.objects.filter(author=user).all()
    






# --------------------------- LIKES/COMMENTS -----------------------------------

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_toggle(request , pk):
    post = get_object_or_404(Post , pk=pk)

    # check if there is an instance of the user liking this post
    like = Like.objects.filter(user=request.user , post=post).first()

    # meaning he already liked this post and wants to remove it
    if like:
        like.delete()
        return Response({"liked": False , "likes_count": post.likes_count} , status=status.HTTP_200_OK)
    
    # he didn't like this post and wants to like
    Like.objects.create(user=request.user , post=post)
    return Response({"liked": True , "likes_count": post.likes_count} , status=status.HTTP_200_OK)



# this view is responsible for creating comments
# get the comments on a specific post
class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk']).all()
    
    def perform_create(self, serializer):
        # just checking if the post actually exists before creating a comment
        post = get_object_or_404(Post , pk=self.kwargs['pk'])
        serializer.save(user=self.request.user , post=post)
        


# this view is responsible for viewing/editing/removing specific comments based on pk
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method in ('PUT' , 'DELETE'):
            return [permissions.IsAuthenticated() , IsOwner()]
        
        return [permissions.IsAuthenticated()]
