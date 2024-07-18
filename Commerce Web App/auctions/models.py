from django.contrib.auth.models import AbstractUser
from django.db import models




class Category(models.Model):
    category_name = models.CharField(max_length = 64)

    def __str__(self):
        return self.category_name

class User(AbstractUser):
    pass

class Bids(models.Model):
    current_bid = models.FloatField()
    user_name = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "User")

    def __str__(self):
        return f"{self.current_bid} by {self.user_name}"

class Auction_listing(models.Model):
    itemname = models.CharField(max_length = 64)
    description = models.CharField(max_length = 300)
    least_bid = models.ForeignKey(Bids, on_delete = models.PROTECT, blank = True, null=True, related_name = "price")
    imageurl = models.CharField(max_length = 1000)
    category = models.ForeignKey(Category,on_delete = models.PROTECT, related_name = "item_category")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "user")
    watchlist = models.ManyToManyField(User, null = True, blank = True, related_name = "watchlist")
    active = models.BooleanField(default = True)
    def __str__(self):
        return self.itemname

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "commenter")
    listing = models.ForeignKey(Auction_listing, on_delete = models.CASCADE, related_name = "listitem")
    comment  = models.CharField(max_length = 1000)

    def __str__(self):
        return f"{self.user} comment on {self.listing}"