from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_entry",views.create, name = "new_entry"),
    path("watchlist", views.watchlist, name="watchlist1"),
    path("category",views.category, name = "category"),
    path("<str:category>",views.specific_category,name = "specific_category"),
    path("listings/<int:id>",views.listing,name = "listings"),
    path("comments/<int:id>",views.comments, name="comments"),
    path("add/<int:id>", views.add, name="add"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("close_auctions/<int:id>", views.close_auctions, name="close_auctions"),
]