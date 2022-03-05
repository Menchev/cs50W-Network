from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# model for a Post
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now=True)

# follow model
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")