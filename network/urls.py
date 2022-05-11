
from django.urls import path

from . import views

urlpatterns = [
    # Pages
    path("", views.index, name="index"),
    path("post", views.post, name="post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    

    # API Routes
    path("new_post", views.new_post, name="new_post"),
    path("posts/<int:page>", views.posts, name="posts"),
    path("posts/<str:user>/<int:page>", views.profile_posts, name="user"),

    path("follow/<str:user>/<str:req_user>", views.follow, name="follow"),
    path("following/<str:user>/<str:req_user>", views.followed, name="followed"),
    path("following_posts/<str:req_user>/<int:page>", views.following_posts, name="following_posts"),
    path("following_count/<str:req_user>", views.following_count, name="following_count"),
    path("follower_count/<str:req_user>", views.follower_count, name="follower_count"),

    path("like/<int:post>", views.getLikes, name="like_count"),
    path("like/<int:post>/<str:user>", views.like, name="like"),
]
