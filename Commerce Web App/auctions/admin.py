from django.contrib import admin
from .models import   Category, User, Auction_listing, Comments,Bids
# Register your models here.

admin.site.register(Auction_listing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Bids)