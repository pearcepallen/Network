
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.post, name="post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    

    # API Routes
    path("new_post", views.new_post, name="new_post"),
    path("posts", views.posts, name="posts"),
    path("posts/<str:user>", views.profile_posts, name="user")
]
