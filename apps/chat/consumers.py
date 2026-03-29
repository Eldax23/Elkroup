from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room
import json


class ChatConsumer(AsyncWebsocketConsumer):

    # triggers when connected to the websocket
    async def connect(self):
        # get the the user who wants to connect to the chat
        self.user = self.scope['user']

        # if he is not authenticated  , stop the connection
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group = f'room__{self.room_id}'

        # check if the user belongs to the conversation
        if not await self.is_member():
            await self.close()
            return

        # adding the connection to the room
        await self.channel_layer.group_add(self.room_group , self.channel_name)
        await self.accept()

        # return json response when successfully connected
        await self.send(json.dumps({
            'type': 'connected',
            'user_id': self.user.id,
            'username': self.user.username,
            'online': True
        }))

    
    # triggers when disconnected from the websocket
    async def disconnect(self, code):
        if hasattr(self,'room_group'):
            await self.send(json.dumps({
                'type': 'disconnect',
                'user_id': self.user.id,
                'username': self.user.username,
                'online': False
            }))
            await self.channel_layer.group_discard(self.room_group , self.channel_name)



@database_sync_to_async
def is_member(self):
    return Room.objects.filter(pk=self.room_id , members=self.user).exists()