from django.contrib import admin

from .models import Person, Coin, BuyAndSell

# Register your models here.
admin.site.register(Person)
admin.site.register(Coin)
admin.site.register(BuyAndSell)