from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max, Count
from datetime import datetime

from .models import User, Bid, Listing, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.annotate(amount=Max("bids__amount"), bidCount=Count("bids")-1),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["starting-bid"]
        imageLink = request.POST["image-link"]
        category = request.POST["category"]
        creationTime = datetime.now().strftime("on %x at %X")
        if title == None or description == None or startingBid == None:
            return render(request, "auctions/register.html", {
                "message": "Please fill out all non-optional fields."
            })
        listing = Listing(title=title, description=description, image=imageLink, category=category, creator=request.user, creationTime=creationTime)
        bid = Bid(bidder=request.user, listing=listing, amount=startingBid, creationTime=creationTime)
        listing.save()
        bid.save()
        return redirect("index")
    else:
        return render(request, "auctions/create.html")
    
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    highestAmount = Bid.objects.filter(listing=listing).aggregate(Max("amount"))
    bid = Bid.objects.filter(listing=listing, amount=int(highestAmount['amount__max'])).get()
    if request.method == "POST":
        amount = request.POST["bid"]
        if amount == None or not amount.isnumeric():
            return render(request, "auctions/listing.html", {
                "message": "Please fill out the bid field with a positive integer."
            })
        if bid.amount >= int(amount):
            return render(request, "auctions/listing.html", {
                "message": "Bid has to excede the price."
            })
        newBid = Bid(bidder=request.user, listing=listing, amount=amount, creationTime=datetime.now().strftime("on %x at %X"))
        newBid.save()
        return redirect("index")
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": bid,
            "bidCount": Bid.objects.filter(listing=listing).count() - 1
        })
