
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("posts", views.compose, name="compose"),
    path("posts/<str:action>/page=<int:pageNo>", views.posts, name ="posting"),
    path("profile/posts/<str:action>/page=<int:pageNo>", views.posts, name ="profilePosting"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("profile/follow/<int:user_id>", views.follow, name="follow"),
]
