
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile_view, name="profile"),
    path("following_posts", views.following_posts_view, name="following_posts"),

    # API routes
    path("edit_post", views.edit_post, name="edit_post"),
]
