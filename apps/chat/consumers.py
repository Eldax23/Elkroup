from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room , Message
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
        # triggers the presence event handler
        await self.channel_layer.group_send(self.room_group , {
            'type': 'presence',
            'user_id': self.user.id,
            'username': self.user.username,
            'online': True
        })

    
    # triggers when disconnected from the websocket
    # which also triggers the presence event handler
    async def disconnect(self, code):
        if hasattr(self,'room_group'):
            await self.channel_layer.group_send(self.room_group , {
                'type': 'presence',
                'user_id': self.user.id,
                'username': self.user.username,
                'online': False
            })
            await self.channel_layer.group_discard(self.room_group , self.channel_name)


    async def receive(self, text_data):
        data = json.loads(text_data)
        # get type of message , chat_message , edit_message , delete_message
        msg_type = data.get('type')

        if msg_type == 'message':
            content = data.get('content' , None).strip()

            if not content:
                # user sent an empty message
                return
            
            # save message to db
            message = await self.save_message_in_db(content)
            await self.channel_layer.group_send(self.room_group , {
                'type': 'chat_message',
                'id': message.id,
                'content': message.content,
                'sender': self.user.username,
                'created_at':message.created_at 
            })

        elif msg_type == 'typing':
            # send a request that triggers the typing_indication event handler function
            await self.channel_layer.group_send(self.room_group , {
                'type': 'typing_indicator',
                'user_id': self.user.id,
                'username': self.user.username,
                'is_typing': True
            })
        
        elif msg_type == 'edit':
            msg_id = data.get('message_id')
            newMessage = data.get('new_message')
            if msg_id:
                msg = await self.edit_message_in_db(msg_id=msg_id , newMessage=newMessage)
                # triggers the message_edited event handler
                await self.channel_layer.group_send(self.room_group , {
                    'type': 'message_edited',
                    'message_id': msg_id,
                    'new_message': newMessage
                })

        elif msg_type == 'deleted':
            msg_id = data.get('message_id')
            if msg_id:
                msg - await self.delete_message_in_db(msg_id=msg_id)
                # triggers the message_deleted event handler
                await self.channel_layer.group_send(self.room_group , {
                    'type': 'message_deleted',
                    'message_id': msg_id,
                })



        
# ----------------------------- event handlers ----------------------------

    async def chat_message(self , event):
     await self.send(text_data=json.dumps({
        'type': 'message',
        'id': event['id'],
        'content': event['content'],
        'sender': event['sender'],
        'created_at': event['created_at']
     }))


    async def typing_indicator(self , event):
     await self.send(text_data = json.dumps({
        'type': 'typing',
        'user_id': event['user_id'],
        'username': event['username'],
        'is_typing': event['is_typing']
     }))



    async def message_edited(self , event):
     await self.send(text_data=json.dumps({
        'type': 'edit',
        'message_id': event['message_id'],
        'new_message': event['new_message']
     }))


    async def message_deleted(self , event):
        await self.send(text_data=json.dumps({
        'type': 'delete',
        'message_id': event['message_id'],
        }))

    async def presence(self , event):
        await self.send(text_data=json.dumps({
            'type': 'presence',
            'user_id': event['user_id'],
            'username': event['username'],
            'online': event['online']
        }))


    # check whether a user a member of this room or no
    @database_sync_to_async
    def is_member(self):
        return Room.objects.filter(pk=self.room_id , members=self.user).exists()

    @database_sync_to_async
    def save_message_in_db(self , content):
    # get the current room
        curr_room = Room.objects.get(pk=self.room_id)

        return Message.objects.create(room=curr_room , sender=self.user , content=content)


    @database_sync_to_async
    def edit_message_in_db(self , msg_id , newMessage):
        try: 
            message = Message.objects.get(pk=msg_id , sender=self.user)
            message.content = newMessage
            message.save()
            return True
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def delete_message_in_db(self , msg_id):
        try:
            message = Message.objects.get(pk=msg_id , sender=self.user)
            message.delete()
            return True
        except Message.DoesNotExist:
            return False
    

