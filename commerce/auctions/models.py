from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()