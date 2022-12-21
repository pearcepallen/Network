import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt


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

@login_required(login_url="login")
def post(request):
    return render(request, "network/post.html") 


def profile(request, user):
    return render(request, "network/profile.html", {
        "profile_user":user
    })


def profile_posts(request, user, page):
    try:
        posts = Post.objects.filter(user__username=user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "No posts found."}, status=404)

    # Return user posts
    if request.method == "GET":
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10) # Show 10 posts per page.

        page_obj = paginator.get_page(page)
        
        data = ({"prev": page_obj.has_previous() and page_obj.previous_page_number() or None,
                "next": page_obj.has_next() and page_obj.next_page_number() or None,
                "data": [page.serialize() for page in page_obj]})
        return JsonResponse(data, safe=False)
        

@login_required(login_url="login")
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

# @login_required(login_url="login")
@csrf_exempt
def edit_post(request, post_user, post_id):
    # New Post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    else:
        try:
            post = Post.objects.get(user__username=post_user, id=post_id)
            data = json.loads(request.body)
            post.content = data['content']
            post.save()
            return JsonResponse({"message": "Content has been updated"})
        except Post.DoesNotExist:
            return JsonResponse({"message": "User cannot edit this post"})

def posts(request, page):
    posts = Post.objects.all()
    if not posts:
        return JsonResponse({"message": "No Posts"}, status=200)
    else:
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10) # Show 10 posts per page.

        page_obj = paginator.get_page(page)
        
        data = ({"prev": page_obj.has_previous() and page_obj.previous_page_number() or None,
                "next": page_obj.has_next() and page_obj.next_page_number() or None ,
                "data": [page.serialize() for page in page_obj]})
        return JsonResponse(data, safe=False)


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
 
# req_user is username
def following_count(request, req_user):
    try:
        f = Following.objects.filter(following__username=req_user).count()
        return JsonResponse({"data": f})
    except Following.DoesNotExist:
        return JsonResponse({"data": "0"})

# req_user is username and not id
def follower_count(request, req_user):
    try:
        user = User.objects.get(username=req_user)
        f = user.following_user.all().count()

        return JsonResponse({"data": f})
    except Following.DoesNotExist:
        return JsonResponse({"data": "0"})


@login_required(login_url="login")
def following_posts(request, req_user, page):
    following = Following.objects.filter(following__username=req_user)
    posts = Post.objects.none() #empty queryset to merge

    for follow in following:
        posts = posts | Post.objects.filter(user=follow.user) #merge querysets

    if not posts:
        return JsonResponse({"message": "No Posts"}, status=200)
    else:
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10) # Show 10 posts per page.

        page_obj = paginator.get_page(page)
        
        data = ({"prev": page_obj.has_previous() and page_obj.previous_page_number() or None,
                "next": page_obj.has_next() and page_obj.next_page_number() or None ,
                "data": [page.serialize() for page in page_obj]})
        return JsonResponse(data, safe=False)


def following(request):
    return render(request, "network/following.html") 



# Like Functions
# post is id of specific post

# Count likes for a post
def get_likes(request, post):
    try:
        post = Post.objects.get(id=post)
        like_count = post.post_likes.all().count()
        return JsonResponse({"likes": like_count})
    except Post.DoesNotExist:
        return JsonResponse({"likes": "0"})

# Like or remove like from post with user
def like(request, post, user):
    try:
        f = Like.objects.get(post__id=post, user__username=user)
        f.delete()
        return JsonResponse({"message": "Like found and deleted. (Unlike)"})     
    except Like.DoesNotExist:
        f = Like(post=Post.objects.get(id=post), user=User.objects.get(username=user))
        f.save()
        return JsonResponse({"message": "Post liked"})





