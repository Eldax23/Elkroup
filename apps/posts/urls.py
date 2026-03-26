from django.urls import path
from . import views

urlpatterns = [
    # feed
    path('feed/' , views.FeedView.as_view() ,name='feed'),
    path('discover/' , views.DiscoverView.as_view() , name='discover'),

    # posts
    path('posts/' , views.PostListCreateAPIView.as_view() , name='posts'),
    path('posts/<int:pk>/' , views.PostDetailView.as_view() , name='post-detail'),
    path('users/<str:username>/posts/' , views.UserPostsView.as_view() , name='user-post')


]