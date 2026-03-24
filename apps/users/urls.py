from django.urls import path
from .views import PostListCreateAPI , UserListCreateAPI


urlpatterns = [
    path('users' , UserListCreateAPI.as_view()),
    path('users/posts' , PostListCreateAPI.as_view())
]