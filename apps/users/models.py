from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/' , blank=True  , null=True, default='profiles/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['username']

    # we now add 2 properties to show following , followers count
    # they are more like shortcuts to get followers,folowing count easily

    @property
    def get_followers_count(self):
        return self.followers.count()
    
    @property
    def get_following_count(self):
        return self.following.count()

# each User uploads -> many posts (one to many)



# follow table has 2 columns
# 1- the follower which is a user (linked to the user table)
# 2- the following which is also a user (linked to the user table)

class Follow(models.Model):
    follower = models.ForeignKey(User , on_delete=models.CASCADE , related_name="following")
    following = models.ForeignKey(User , on_delete=models.CASCADE , related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


