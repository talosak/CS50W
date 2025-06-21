from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Count

from .models import User, FlashSet, Flashcard, Settings

def index(request):
    # Order the flashsets while checking if user is logged in
    try:
        if request.user.settings.flashSetDisplayOrder == "likes":
            order = "-likeCount"
        elif request.user.settings.flashSetDisplayOrder == "name":
            order = "name"
        elif request.user.settings.flashSetDisplayOrder == "newest":
            order = "-timestamp"
        elif request.user.settings.flashSetDisplayOrder == "creator":
            order = "-creator__name"
        else:
            order = "-timestamp"
    except AttributeError:
        order = "-timestamp"

    flashsets = FlashSet.objects.annotate(likeCount=Count("likers"), flashcardCount=Count("flashcards")).order_by(order).all()
    return render(request, "taloflash/index.html", {
        "sets": flashsets,
    })

def createFlashcard(request, set_id):
    if request.method == "POST":
        flashset = FlashSet.objects.annotate(likeCount=Count("likers"), flashcardCount=Count("flashcards")).get(pk=set_id)
        creator = request.user
        front = request.POST["front"]
        back = request.POST["back"]
        imageURL = request.POST["imageURL"]

        # Ensure both sides aren't blank
        if front == "" or back == "":
            messages.error(request, "Both sides of the flashcard must be inputted")
            return render(request, "taloflash/createFlashcard.html", {
                "flashset": flashset,
            })
        
        flashcard = Flashcard(creator=creator, front=front, back=back, imageURL=imageURL, flashSet_id=flashset.id)
        flashcard.save()
        messages.success(request, "Flashcard created successfully")
        return redirect("set", set_id=set_id)
    else:
        flashset = FlashSet.objects.annotate(likeCount=Count("likers"), flashcardCount=Count("flashcards")).get(pk=set_id)
        return render(request, "taloflash/createFlashcard.html", {
            "flashset": flashset,
        })
    

def createSet(request):
    if request.method == "POST":
        creator = request.user
        name = request.POST["name"]
        description = request.POST["description"]

        # Ensure name isn't blank
        if name == "":
            messages.error(request, "FlashSet's name is missing")
            return render(request, "taloflash/createSet.html")

        # Create the flashset
        flashset = FlashSet(creator=creator, name=name, description=description)
        flashset.save()
        flashset.editors.add(creator)
        flashset.save()
        messages.success(request, "Set created successfully")
        return redirect("index")
    else:
        return render(request, "taloflash/createSet.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "taloflash/login.html")
    
    elif request.user.is_authenticated:
        # User is already logged in
        messages.error(request, "Already logged in")
        return redirect("index")
    else:
        return render(request, "taloflash/login.html")
    
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("index")
    
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            messages.error(request, "Password must match confirmation")
            return render(request, "taloflash/register.html")
        
        # Ensure username is unique
        try:
            user = User.objects.create_user(username=username, email="", password=password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken")
            return render(request, "network/register.html")
        
        # Create settings
        settings = Settings(user=user)
        settings.save()

        login(request, user)
        messages.success(request, "Registered successfully")
        return redirect("index")
    
    elif request.user.is_authenticated:
        # User is already logged in
        messages.error(request, "Already logged in")
        return redirect("index")

    else:
        return render(request, "taloflash/register.html")

def set_view(request, set_id):
        if request.method == "POST":
            # Delete Flashset
            flashset = FlashSet.objects.get(pk=set_id)
            flashset.delete()
            messages.success(request, "Set deleted successfully")
            return redirect("index")
        else:
            flashset = FlashSet.objects.annotate(likeCount=Count("likers"), flashcardCount=Count("flashcards")).get(pk=set_id)
            flashcards = Flashcard.objects.filter(flashSet=flashset).all()
            return render(request, "taloflash/flashset.html", {
                "flashset": flashset,
                "flashcards": flashcards,
            })
