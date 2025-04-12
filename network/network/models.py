from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", blank=True, related_name="followedUsers")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [follower.id for follower in self.followers.all()],
            "followedUsers": [followedUser.id for followedUser in self.followedUsers.all()],
        }

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdPosts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, blank=True, related_name="likedPosts")

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.serialize(),
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likers": [liker.id for liker in self.likers.all()]
        }

