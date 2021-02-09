import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse


from .models import *


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


def post(request):
    return render(request, "network/post.html") 


def profile(request, user):
    return render(request, "network/profile.html", {
        "profile_user":user
    })


def profile_posts(request, user):
    try:
        posts = Post.objects.filter(user__username=user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "No posts found."}, status=404)

    # Return user posts
    if request.method == "GET":
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)


def new_post(request):
    # New Post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    data = json.loads(request.body)
    post = Post(
        user = request.user,
        content = data.get("content", "")
    )
    post.save()

    return JsonResponse({"message": "Successfully posted."}, status=201)


def posts(request):
    posts = Post.objects.all()
    if not posts:
        return JsonResponse({"message": "No Posts"}, status=200)
    else:
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)


def follow(request, user, req_user):
    #Check if user is already followed by request.user
    try:
        f = Following.objects.get(user__username=user, following__username=req_user)
    except Following.DoesNotExist:
        f = Following(user=User.objects.get(username=user), following=User.objects.get(username=req_user))
        f.save()
        return JsonResponse({"message": "User followed"})

    #Delete entry if already followed
    f.delete()
    return JsonResponse({"message": "User unfollowed"})


def followed(request, user, req_user):
    #Check if user is already followed by request.user
    try:
        f = Following.objects.get(user__username=user, following__username=req_user)
    except Following.DoesNotExist:
        #Return false if user is not following
        return JsonResponse({"follow":False})

    #Return true entry if user is followed
    return JsonResponse({"follow":True})


@login_required(login_url="login")
def following_posts(request, req_user):
    following = Following.objects.filter(following__username=req_user)
    posts = []

    for follow in following:
        posts.extend(Post.objects.filter(user=follow.user))

    if not posts:
        return JsonResponse({"message": "No Posts"}, status=200)
    else:
        #posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)


def following(request):
    return render(request, "network/following.html") 


