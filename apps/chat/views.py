from django.shortcuts import render , get_object_or_404


from rest_framework import generics
from .serializers import RoomSerializer , MessageSerializer
from .models import Room
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
