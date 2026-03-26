from django.shortcuts import render
from rest_framework import generics , status , permissions
from rest_framework.response import Response
from .serializers import PostSerializer , CreatePostSerializer
from .models import Post


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
    
    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [permissions.IsAuthenticated]
        
    #     return [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # adding 'author' since its not included in the CreatePostSerializer
        # and setting it to the current user
        post = serializer.save(author=self.request.user)
        return Response(PostSerializer(post , context={'request': request}).data , status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]



