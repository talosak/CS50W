from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
# API route
@csrf_exempt
def posts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")
        creator = request.user
        post = Post(creator=creator, content=content)
        post.save()
        redirect("index")
        return JsonResponse({"message": "Post created successfully."}, status=201)
    else:
        # Get all posts
        posts = Post.objects.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)
    
def profile(request, user_id):
    # Get user
    try:
        profile = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    if request.method == "POST":
        if request.POST["formType"] == "follow":
            profile.followers.add(request.user)
            return redirect("profile", user_id=user_id)
        else:
            profile.followers.remove(request.user)
            return redirect("profile", user_id=user_id)
    else:        
        return render(request, "network/profile.html", {
            "profile": User.objects.filter(pk=user_id).annotate(followerCount=Count("followers"), followedUserCount=Count("followedUsers")).get()
        })

@csrf_exempt  
def following(request):
    if request.method == "POST":
        currentUser = User.objects.get(pk=request.user.id)
        followedUsers = currentUser.followedUsers.all()
        return JsonResponse([followedUser.serialize() for followedUser in followedUsers], safe=False)
    else:
        if not request.user.is_authenticated:
            return redirect("index")
        return render(request, "network/following.html")

@csrf_exempt 
def paginate(request):
    data = json.loads(request.body)
    paginator = Paginator(data.get("postList", ""), 10)
    page = paginator.page(int(data.get("page_id", "")))
    try:
        next_page_number = page.next_page_number()
    except:
        next_page_number = "None"
    try:
        previous_page_number = page.previous_page_number()
    except:
        previous_page_number = "None"
    serializedPage = {
        "str": str(page),
        "list": page.object_list,
        "hasNext": page.has_next(),
        "hasPrevious": page.has_previous(),
        "nextPageNumber": next_page_number,
        "previousPageNumber": previous_page_number
    }
    return JsonResponse(serializedPage)