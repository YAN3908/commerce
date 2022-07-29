from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Lot, Category, Bid, Comit

# Register your models here.
class users_bid(admin.ModelAdmin):
    filter_horizontal = ("price",)

class commit(admin.ModelAdmin):
    filter_horizontal = ("user_comit",)

User = get_user_model()

admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Lot, users_bid)
admin.site.register(User)
admin.site.register(Comit)



