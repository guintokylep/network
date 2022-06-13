import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User
from .models import Profile
from .models import Posts


def index(request):

    posting = Posts.objects.all

    return render(request, "network/index.html", {
        "post": posting
    })
    
def posts(request, action):

    if action == "allposts":
        posting = Posts.objects.all()
    
    posting = posting.order_by("-date").all()
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

    return JsonResponse({"message": "Email sent successfully."}, status=201)

@csrf_exempt
@login_required
def profile(request, user_id):

    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
    else:
        return render(request, "network/login.html")

    return render(request, "network/profile.html", {
        "username": user.username
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
    
