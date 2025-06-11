from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError

from .models import User, FlashSet, Flashcard, Settings

def index(request):
    return render(request, "taloflash/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "taloflash/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "taloflash/login.html")
    
def logout_view(request):
    logout(request)
    return redirect("index")
    
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "taloflash/register.html", {
                "messageError": "Password must match confirmation"
            })
        
        # Ensure username is unique
        try:
            user = User.objects.create_user(username=username, email="", password=password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return redirect("index")

    else:
        return render(request, "taloflash/register.html")
