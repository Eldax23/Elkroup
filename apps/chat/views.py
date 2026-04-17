from django.shortcuts import render


from rest_framework import generics
from .serializers import RoomSerializer
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
