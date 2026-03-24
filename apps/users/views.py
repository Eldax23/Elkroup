from django.shortcuts import render
from rest_framework import generics , status , permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
# Create your views here.


from .models import Post , User

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