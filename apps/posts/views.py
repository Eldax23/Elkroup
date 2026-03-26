from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer
from .models import Post


# Create your views here.


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
