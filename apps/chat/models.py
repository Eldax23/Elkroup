from django.db import models
from apps.users.models import User

# Create your models here.



# this is the Room model which holds all conversations between users
# could be a group or a dm
class Room(models.Model):
    # the name of the conversation (group name)
    # if its a group then it holds the group name
    name = models.CharField(max_length=50 , blank=True)

    # contains the people who participates in this convo (could be 2 or more)
    # user -> many convos , convo -> many users (many to many)
    participants = models.ManyToManyField(User , blank=True , related_name="chat_rooms")


    # clarifies whether this is a groupchat or a dm
    is_dm = models.BooleanField(default=False)

    # denotes the user who created this room (conversation)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL , related_name="created_chats")

    created_at = models.DateTimeField(auto_now_add=True)




class Message:

    content = models.TextField()

    # the user who sent this message
    # user sends (many) messages (one-to-many)
    sender = models.ForeignKey(User , on_delete=models.CASCADE , related_name='sent_messages')

    # the room this message got sent in
    room = models.ForeignKey(Room , on_delete=models.CASCADE , related_name='messages')

    created_at = models.DateTimeField(auto_now_add=True)

