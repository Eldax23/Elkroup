from django.shortcuts import render
from rest_framework import generics
# Create your views here.


from .models import Post , User

from .serializers import PostSerializer , UserSerializer


class PostListCreateAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserListCreateAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
