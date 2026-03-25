from django.shortcuts import render
from rest_framework import generics , status , permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from django.shortcuts import get_object_or_404
# Create your views here.


from .models import Post , User , Follow

from .serializers import PostSerializer , UserSerializer , RegisterSerializer , UpdateProfileSerializer


class PostListCreateAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer





# this serializer is only for registering users to the system
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # get the referesh token and access token for the current user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({
            # serialize the current user and return it in the response.
            'user': UserSerializer(user , context={'request': request}).data,
            'tokens': {
                'refresh': f"{refresh}",
                'access': f"{access}"
            }
        } , status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        # obtain the token from the request
        refresh_token = request.data['refresh']

        # create a RefreshToken Object from it
        token = RefreshToken(refresh_token)

        # block the token 
        token.blacklist()
        return Response({"message": "Logged out successfully."} , status=status.HTTP_200_OK)
    except(KeyError , TokenError):
        return Response({'message': "Invalid Token"} , status=status.HTTP_400_BAD_REQUEST)







# later after registering the user u can update the profile
class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer
    lookup_field = 'pk'



# this is when the user goes to his profile , he can either 
# 1- update his profile
# 2- just check his profile details 
# it depends on the request type

class MyProfileView(generics.RetrieveUpdateAPIView):
    def get_serializer_class(self):
        # we check the request type
        if(self.request.method == 'PUT'):
            # if its a PUT request then we use the appropriate serializer
            return UpdateProfileSerializer
        
        # otherwise since its not a PUT request we just want the details
        return UserSerializer
    

    # we override the get_object method to automatically detect the 
    # currently logged in user and get the instance which we will 
    # do all the work on


    def get_object(self):
        return self.request.user



class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
# this request is initiaited from the currently logged in user
# the username of the person to follow
# this is a toggle ,  meaning if he was already following he will unfollow and the opposite
def follow_toggle(request , username):
    person_to_follow = get_object_or_404(User , username=username)
    
    # meaning he tried to follow himself
    if person_to_follow == request.user:
        return Response({"detail": "you can't follow yourself"})
    
    # check if he is already following
    follow = Follow.objects.filter(follower=request.user ,
         following=person_to_follow).first()
    
    if follow:
        # if he is following , unfollow.
        follow.delete()
        return Response({'following': False})
    

    # otherwise he wants to follow the person   
    Follow.objects.create(follower=request.user , following=person_to_follow)
    return Response({'following': True})
