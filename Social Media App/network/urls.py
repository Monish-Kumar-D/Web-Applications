
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("following", views.following_posts, name="following"),
    path("edit/<int:edit_id>", views.edit, name="edit"),
    path('follow/<int:profile_id>', views.follow, name='follow'),
    path('unfollow/<int:profile_id>', views.unfollow, name='unfollow'),
    path('like/<int:post_id>', views.like_post, name='like_post'),
]
