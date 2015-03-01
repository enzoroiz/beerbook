from django.contrib import admin
from beerbookapp.models import Beer, BeerType, BeerProducer, Event, Rating
from beerbookapp.models import Location, City, Pub, PubStockItem, FriendListItem

# Register your models here.

admin.site.register(Beer)
admin.site.register(BeerType)
admin.site.register(BeerProducer)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(City)
admin.site.register(Pub)
admin.site.register(PubStockItem)
admin.site.register(Rating)
admin.site.register(FriendListItem)
