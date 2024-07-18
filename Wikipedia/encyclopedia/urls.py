from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name = "search"),
    path("addnew", views.add, name="addnew"),
    path("random", views.rand, name="random"),
    path("<str:title>", views.title, name="title"),
    path("edit/<str:title>", views.edit, name="edit"),
]
