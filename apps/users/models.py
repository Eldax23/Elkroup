from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = ['username']

# each User uploads -> many posts

class Post(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



# for each like there is: somebody who liked the post (USER)
# and the post itself (POST)
class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)


# same thing for comment but there is the comment content itself
# and the date it was created
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
