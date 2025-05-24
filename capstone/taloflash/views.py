from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import User, FlashSet, Flashcard, Settings

def index(request):
    return render(request, "taloflash/index.html")

def login_view(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "taloflash/login.html")
    
def logout_view(request):
    logout(request)
    return redirect("index")
    
def register(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "taloflash/register.html")
