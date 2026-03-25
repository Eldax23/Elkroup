from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True , validators = [validate_password])
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password')

    def create(self, validated_data):
        # here we must hash the password
        return User.objects.create_user(**validated_data)

    

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username' , 'bio' , 'profile_pic')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id' , 'email' , 'username' , 'bio' , 'profile_pic'
                  , 'created_at')
        