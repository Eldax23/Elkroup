from django.db import models
from apps.users.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts_pics/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return self.comments.count()
    
    def __str__(self):
        return f"author: {self.author} posted {self.content}"



# user -> likes (one to many)
# for each like there is: somebody who liked the post (USER)
# and the post itself (POST)
class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='likes')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='likes')

    def __str__(self):
        return f"{self.user.username} liked {self.post.pk}"

# user -> many comments (one to many)
# same thing for comment but there is the comment content itself
# and the date it was created
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name='comments')
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} commented on post {self.post_id}"

