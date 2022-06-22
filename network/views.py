import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils import timezone

from .models import User
from .models import Profile
from .models import Posts


def index(request):
    posting = Posts.objects.all()

    return render(request, "network/index.html",{
        "noOfPost": posting
    })

def following(request):
    user_ids = Profile.objects.get(userId=request.user.id)
    user_ids = user_ids.following.all()
    posting = 0
    if user_ids.count() != 0:
        posting = Posts.objects.filter(postUser__in=user_ids) 
        posting = posting.order_by("-date").all()
        posting = posting.count

    
    return render(request, "network/following.html",{
        "noOfPost": posting
    })

def posts(request, action, pageNo):
    
    hasPost = False
    posting = []

    if action == "allposts":
        posting = Posts.objects.all()
        hasPost = True
    elif action == "following":
        user_ids = Profile.objects.get(userId=request.user.id)
        user_ids = user_ids.following.all()
        
        if user_ids.count() != 0:
            posting = Posts.objects.filter(postUser__in=user_ids)
            hasPost = True
        
    else:
        posting = Posts.objects.filter(postUser=action)
        hasPost = True
    
    if hasPost :
        posting = posting.order_by("-date").all()
        posting = Paginator(posting,10)
        posting = posting.page(pageNo).object_list
    
    return JsonResponse([postsDisplay.serialize() for postsDisplay in posting], safe=False)

@csrf_exempt
@login_required
def compose(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    composePost = Posts(
        postUser=request.user,
        postDescription=data.get("body", "")
    )
    composePost.save()

    posting = Posts.objects.all()

    return JsonResponse({
        "message": "Posted successfully.",
        "noOfPost": posting.count()
    }, status=201)

@csrf_exempt
@login_required
def edit(request, post_no):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    post = Posts.objects.get(id=post_no,postUser=request.user)
    post.postDescription = data
    post.save()

    posting = Posts.objects.filter(id=post_no,postUser=request.user)

    return JsonResponse([postsDisplay.serialize() for postsDisplay in posting], safe=False)

def profile(request, user_id):

    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(userId=user_id)
        posting = Posts.objects.filter(postUser=user_id)
    else:
        return render(request, "network/login.html")

    return render(request, "network/profile.html", {
        "loginUser": request.user,
        "userId": user_id,
        "username": user.username,
        "followers": profile.followers.all(),
        "following": profile.following.all(),
        "posting": posting.order_by("date").all(), 
        "follow": True if profile.followers.filter(id=request.user.id).count() != 0 else False  
    })

def unfollow(request, user_id):
    #login users following update
    logingUserFollowing = Profile.objects.get(userId=request.user.id)
    logingUserFollowing.following.remove(user_id)

    #following users followers update
    userFollowing = Profile.objects.get(userId=user_id)
    userFollowing.followers.remove(request.user.id)

    return JsonResponse({"followers": userFollowing.followers.all().count()})

def follow(request, user_id):
    #login users follow update
    logingUserFollowing = Profile.objects.get(userId=request.user.id)
    logingUserFollowing.following.add(user_id)

    #follow users followers update
    userFollow = Profile.objects.get(userId=user_id)
    userFollow.followers.add(request.user.id)

    return JsonResponse({"followers": userFollow.followers.all().count()})

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
            profile = Profile(
                    userId=user
                )
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
