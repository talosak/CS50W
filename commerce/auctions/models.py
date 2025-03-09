from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    creationTime = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.title} by {self.creator}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    creationTime = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.amount}$ by {self.bidder} for {self.listing}"
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    creationTime = models.DateTimeField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return f"{self.id}: comment under {self.listing} by {self.creator}"