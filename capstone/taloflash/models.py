from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }
    
class FlashSet(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createdSets")
    editors = models.ManyToManyField(User, related_name="editableSets")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(User, related_name="likedSets")
    savers = models.ManyToManyField(User, related_name="savedSets")
    
class Flashcard(models.Model):
    flashSet = models.ForeignKey(FlashSet, on_delete=models.CASCADE, related_name="flashcards")
    front = models.CharField(max_length=255)
    back = models.CharField(max_length=255)
    imageURL = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="createdFlashcards")
    learners = models.ManyToManyField(User, related_name="learnedFlashcards")

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    theme = models.CharField(default="dark", choices=[("dark", "Dark"), ("light", "Light")], max_length=63)
    flashSetDisplayOrder = models.CharField(default="newest", choices=[("likes", "Most liked"), ("name", "Name"), ("newest", "Newest"), ("creator", "Creator's name")], max_length=63)
    flashcardDisplayOrder = models.CharField(default="random", choices=[("random", "Random"), ("ordered", "Ordered")], max_length=63)
    flashcardFontSize = models.IntegerField(default=16)
    showTimer = models.BooleanField(default=False)
    timeLimit = models.IntegerField(default=0)
    backToForwardMode = models.BooleanField(default=False)
    postFlipCooldown = models.FloatField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "userID": self.user.id,
            "theme": self.theme,
            "flashcardDisplayOrder": self.flashcardDisplayOrder,
            "flashcardFontSize": self.flashcardFontSize,
            "showTimer": self.showTimer,
            "timeLimit": self.timeLimit,
            "backToForwardMode": self.backToForwardMode,
            "postFlipCooldown": self.postFlipCooldown
        }

