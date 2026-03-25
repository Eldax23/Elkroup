from django.urls import path
from . import views

urlpatterns = [
    # posts
    path('users/posts' , views.PostListCreateAPI.as_view() , name='posts')

]