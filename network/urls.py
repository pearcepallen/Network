
from django.urls import path

from . import views

urlpatterns = [
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
    path("posts/<str:user>", views.profile_posts, name="user"),
    path("follow/<str:user>/<str:req_user>", views.follow, name="follow"),
    path("following/<str:user>/<str:req_user>", views.followed, name="followed"),
    path("following_posts/<str:req_user>", views.following_posts, name="following_posts")
    # path("page_posts/<int:page>", views.page_posts, name="page_posts")
]
