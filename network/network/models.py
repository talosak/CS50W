from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", blank=True, related_name="followedUsers")

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdPosts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, blank=True, related_name="likedPosts")

