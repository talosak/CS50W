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
    flashSetDisplayOrder = models.CharField(default="likes", choices=[("likes", "Most liked"), ("name", "Name"), ("newest", "Newest"), ("creator", "Creator's name")], max_length=63)
    flashcardDisplayOrder = models.CharField(default="random", choices=[("random", "Random"), ("oldest", "Oldest"), ("alphabeticalFront", "Alphabetical - front side)"), ("alphabeticalBack", "Alphabetical - back side")], max_length=63)
    flashcardFontSize = models.IntegerField(default=64)
    showTimer = models.BooleanField(default=False)
    timeLimit = models.IntegerField(default=0)
    timerBehavior = models.CharField(default="countDown", choices=[("countDown", "Count down"), ("countUp", "Count up")], max_length=63)
    timeLimitBehavior = models.CharField(default="nothing", choices=[("nothing", "Nothing"), ("show", "Show"), ("kick", "Kick"), ("restart", "Restart")], max_length=63)
    postFlipCooldown = models.FloatField(default=0)
    backToForwardMode = models.BooleanField(default=False)
    hardcoreMode = models.BooleanField(default=False)

