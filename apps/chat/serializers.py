from rest_framework import serializers
from .models import Message , Room
from apps.users.serializers import UserSerializer

class RoomSerializer(serializers.ModelSerializer):
    # current members of the chat
    members = UserSerializer(many=True , read_only=True)
    class Meta:
        model = Room
        fields = ('id' , 'name' , 'members' , 'is_dm' , 'created_at')



class MessageSerializer(serializers.ModelSerializer):
    # the user who sent the message
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ('id' , 'content' , 'sender', 'created_at')
        read_only_fields = ('id' , 'sender' , 'created_at')


