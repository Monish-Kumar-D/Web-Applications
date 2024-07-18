from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models

from .models import User


def index(request):
    if request.method == "GET":
         contents = models.Auction_listing.objects.all()
         return render(request, "auctions/index.html",{
             "contents" : contents
         })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        itemname = request.POST["itemname"]
        price = request.POST["least_bid"]
        category = request.POST["category"]
        link = request.POST["imageurl"]
        #if link == NULL:
            #link
        description = request.POST["description"]
        category1 = models.Category.objects.get(category_name=category)
        currentUser = request.user
        bid = models.Bids(current_bid = price, user_name = currentUser)
        bid.save()
        newlisting = models.Auction_listing(
            itemname = itemname,
            description = description,
            least_bid = bid,
            imageurl = link,
            category = category1,
            owner = currentUser
        )
        newlisting.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        categorys = models.Category.objects.all()
        return render(request, "auctions/new_entry.html",{"categorys" : categorys})

def category(request):

    categorys = models.Category.objects.all()
    if request.method == "GET":
        return render(request,"auctions/category.html",{"categorys" : categorys})


def specific_category(request,category):
    categorys = models.Category.objects.filter(category_name = category).values_list('id', flat=True)
    contents = models.Auction_listing.objects.filter(category_id = categorys[0]).all
    return render(request, "auctions/index.html",{
             "contents" : contents
         })

def listing(request,id):
    listing1 = models.Auction_listing.objects.get(pk = id)
    comments1 = models.Comments.objects.filter(listing = listing1).all
    inwatchlist = request.user in listing1.watchlist.all()
    isthisowner = request.user.username == listing1.owner.username
    contents1 = models.Auction_listing.objects.filter(id = id).all
    if request.method == "GET":
        return render(request, "auctions/listings.html",{
                "contents" : contents1,
                "inwatchlist" : inwatchlist,
                "comments" : comments1,
                "isthisowner" : isthisowner
            })
    else:
        contents = models.Auction_listing.objects.get(pk = id)
        price = float(request.POST["least_bid"])
        if contents.least_bid.current_bid >= price:
           return render(request, "auctions/listings.html",{
                "contents" : contents1,
                "message" : "Price is not sffecicent",
                "comments" : comments1,
                "isthisowner" : isthisowner
            })
        else:
            contents.least_bid.current_bid = price
            contents.least_bid.user_name = request.user
            contents.least_bid.save()
            contents.save()
            return render(request,"auctions/listings.html",{
                "contents" : contents1,
                "message" : "Price Updated",
                "comments" : comments1,
                "isthisowner" : isthisowner
              })

def close_auctions(request,id):
    contents = models.Auction_listing.objects.get(pk = id)
    contents.active = False
    contents.save()
    isthisowner = request.user.username == contents.owner.username
    comments1 = models.Comments.objects.filter(listing = contents).all
    contents1 = models.Auction_listing.objects.filter(id = id).all
    return render(request,"auctions/listings.html",{
                "contents" : contents1,
                "message" : "Auction Closed!",
                "comments" : comments1,
                "isthisowner" : isthisowner,
              })

def watchlist(request):
    if request.method == "GET":
        user = request.user
        watchlist1 = user.watchlist.all()
        return render(request, "auctions/hello.html",{
            "watchlist" : watchlist1
        })


def comments(request,id):
    if request.method == "POST":
        comment1 = request.POST['comments']
        user = request.user
        listings1 = models.Auction_listing.objects.get(pk=id)
        newcomment = models.Comments(
            user = user,
            listing = listings1,
            comment = comment1
        )
        newcomment.save()
        return HttpResponseRedirect(reverse("listings",args=(id, )))


def add(request,id):
    listing1 = models.Auction_listing.objects.get(pk = id)
    user = request.user
    listing1.watchlist.add(user)
    return HttpResponseRedirect(reverse("listings",args=(id, )))

def remove(request,id):
    listing1 = models.Auction_listing.objects.get(pk = id)
    user = request.user
    listing1.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listings",args=(id, )))