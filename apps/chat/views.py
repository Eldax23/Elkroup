from django.shortcuts import render , get_object_or_404

from rest_framework import generics , status , permissions
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .serializers import RoomSerializer , MessageSerializer , CreateDMSerializer
from .models import Room
from apps.users.models import User
# Create your views here.


# list all available rooms
class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class RoomDetailView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        # only get the room which the user who issued the request are part of
        return Room.objects.filter(members=self.request.user)
    

class MessageHistoryView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        # fetching the room in which its id got sent in the url  , and the user is also a member of
        room = get_object_or_404(Room , pk=self.kwargs['room_id'] , members=self.request.user)
        # get all the messages of that room and fetch the sender aswell
        return room.messages.select_related('sender').all()
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_dm(request):
    # start or retrieve a dm between the user who sent this request and another user
    serializer = CreateDMSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # the other user 
    target = get_object_or_404(User , username=serializer.validated_data['username'])

    # then the user tried to create a dm with himself
    if request.user == target:
        return Response({'detail': 'you cannot dm yourself'} , status=400)
    
    room , created = Room.get_or_create_dm(request.user , target)

    return Response(
        RoomSerializer(room , context={'request':request}).data,
        status=201 if created else 200
    )
