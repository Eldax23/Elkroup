from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView


urlpatterns = [
    # auth
    path('auth/register/' , views.RegisterView.as_view() , name='register'),
    path('auth/login/' , TokenObtainPairView.as_view() , name = 'login'),
    path('auth/refresh/' , TokenRefreshView.as_view() , name = 'refresh_token'),
    path('auth/logout/' , views.logout_view),
    # profiles
    path('users/myprofile/' , views.MyProfileView.as_view() , name = 'my_profile'),
    path('users/<str:username>/' , views.UserProfileView.as_view() , name ='profile'),

    # following

    # posts
    path('users/posts' , views.PostListCreateAPI.as_view() , name='posts')
]