from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max, Count, Min
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import User, Bid, Listing, Comment

categoryList = ["Unspecified", "Fashion", "Toys", "Electronics", "Home", "Tomfoolery"]

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.annotate(amount=Max("bids__amount"), bidCount=Count("bids")-1).order_by('-id').values(),
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
    
@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["starting-bid"]
        imageLink = request.POST["image-link"]
        if request.POST["category"]:
            category = request.POST["category"]
        else:
            category = None
        creationTime = datetime.now().strftime("on %x at %X")
        if title == "" or description == "" or startingBid == "":
            return render(request, "auctions/create.html", {
                "message": "Please fill out all non-optional fields.",
                "categories": categoryList,
            })
        if startingBid == "" or not startingBid.isnumeric():
            return render(request, "auctions/listing.html", {
                "message": "Please fill out the bid field with a positive integer.",
                "listing": listing,
                "bid": bid,
                "bidCount": Bid.objects.filter(listing=listing).count() - 1,
                "comments": Comment.objects.filter(listing=listing).all().order_by('-id'),
            })
        listing = Listing(title=title, description=description, image=imageLink, category=category, creator=request.user, creationTime=creationTime, isActive=True, startingPrice=startingBid)
        bid = Bid(bidder=request.user, listing=listing, amount=startingBid, creationTime=creationTime)
        listing.save()
        bid.save()
        return redirect("index")
    else:
        return render(request, "auctions/create.html", {
            "categories": categoryList,
        })
    
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    highestAmount = Bid.objects.filter(listing=listing).aggregate(Max("amount"))
    if Bid.objects.filter(listing=listing, amount=int(highestAmount['amount__max'])).count() > 1:
        first = Bid.objects.filter(listing=listing, amount=int(highestAmount['amount__max'])).aggregate(Min("id"))
        bid = Bid.objects.filter(listing=listing, amount=int(highestAmount['amount__max'])).exclude(pk=first['id__min']).get()
    else:
        bid = Bid.objects.filter(listing=listing, amount=int(highestAmount['amount__max'])).get()
    if request.method == "POST" and request.POST["formType"] == "formWatchlist":
        if request.user in listing.watchers.all():
            listing.watchers.remove(request.user)
            listing.save()
        else:
            listing.watchers.add(request.user)
            listing.save()
        return redirect("listing", listing_id=listing.id)
    elif request.method == "POST" and request.POST["formType"] == "formClose":
        listing.isActive = False
        listing.save()
        return redirect("listing", listing_id=listing.id)
    elif request.method == "POST" and request.POST["formType"] == "formComment":
        content = request.POST["comment"]
        if content == "":
            return render(request, "auctions/listing.html", {
                "message": "Please fill out the comment field before submitting a comment.",
                "listing": listing,
                "bid": bid,
                "bidCount": Bid.objects.filter(listing=listing).count() - 1,
                "comments": Comment.objects.filter(listing=listing).all().order_by('-id'),
            })
        comment = Comment(creator=request.user, listing=listing, content=content,creationTime=datetime.now().strftime("on %x at %X"))
        comment.save()
        return redirect("index")
    elif request.method == "POST":
        amount = request.POST["bid"]
        if amount == "" or not amount.isnumeric():
            return render(request, "auctions/listing.html", {
                "message": "Please fill out the bid field with a positive integer.",
                "listing": listing,
                "bid": bid,
                "bidCount": Bid.objects.filter(listing=listing).count() - 1,
                "comments": Comment.objects.filter(listing=listing).all().order_by('-id'),
            })
        if int(amount) < bid.amount and Bid.objects.filter(listing=listing).count() - 1 == 0:
            return render(request, "auctions/listing.html", {
                "message": "Bid has to excede or match the starting price.",
                "listing": listing,
                "bid": bid,
                "bidCount": Bid.objects.filter(listing=listing).count() - 1,
                "comments": Comment.objects.filter(listing=listing).all().order_by('-id'),
            })
        if int(amount) <= bid.amount and Bid.objects.filter(listing=listing).count() - 1 != 0:
            return render(request, "auctions/listing.html", {
                "message": "Bid has to excede the current bid.",
                "listing": listing,
                "bid": bid,
                "bidCount": Bid.objects.filter(listing=listing).count() - 1,
                "comments": Comment.objects.filter(listing=listing).all().order_by('-id'),
            })
        newBid = Bid(bidder=request.user, listing=listing, amount=amount, creationTime=datetime.now().strftime("on %x at %X"))
        newBid.save()
        return redirect("index")
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": bid,
            "bidCount": Bid.objects.filter(listing=listing).count() - 1,
            "comments": Comment.objects.filter(listing=listing).all().order_by('-id'),
        })

@login_required    
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.filter(watchers=request.user).annotate(amount=Max("bids__amount"), bidCount=Count("bids")-1).order_by('-id').values()
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": categoryList,
    })

def categoriesResults(request, category):
    return render(request, "auctions/categoriesResults.html", {
        "category": category,
        "listings": Listing.objects.filter(category=category).annotate(amount=Max("bids__amount"), bidCount=Count("bids")-1).order_by('-id').values()
    })