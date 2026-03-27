from django.urls import path
from . import views

urlpatterns = [
    # feed
    path('feed/' , views.FeedView.as_view() ,name='feed'),
    path('discover/' , views.DiscoverView.as_view() , name='discover'),

    # posts
    path('posts/' , views.PostListCreateAPIView.as_view() , name='posts'),
    path('posts/<int:pk>/' , views.PostDetailView.as_view() , name='post-detail'),
    path('users/<str:username>/posts/' , views.UserPostsView.as_view() , name='user-post'),
    # likes
    path('posts/<int:pk>/like/' , views.like_toggle , name='like'),

    # comments
    path('posts/<int:pk>/comments/' , views.CommentListCreateView.as_view() , name='comment'),
    path('comments/<int:pk>/' , views.CommentDetailView.as_view() , name='comment-detail'),



]