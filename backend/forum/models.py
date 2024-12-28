from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


# class User(AbstractUser):
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Thread(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# class Forum(models.Model):
#     ForumTitle = models.CharField(max_length=100)
#     def GetPosts(self):
#         return self.posts.all()
#     def createPost(self,user,content):
#         return
#     def Reply(self,postID,content):
#         return
#
# class Post(models.Model):
#     #postID = models.IntegerField(max_length=30)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     forum = models.ForeignKey(Forum,on_delete=models.CASCADE,related_name='posts')
#     content = models.CharField(max_length=5000)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def addReply(self, reply):
#         return
#
# class Reply(models.Model):
#     #replyID = models.IntegerField(max_length=30)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post,on_delete=models.CASCADE)
#     content = models.CharField(max_length=5000)
#     created_at = models.DateTimeField(auto_now_add=True)
