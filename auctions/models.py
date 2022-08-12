from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # userLot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="userLot")
    pass


class Category(models.Model):
    category = models.CharField(max_length=64)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biduser")
    price = models.IntegerField()
    time_lot = models.DateTimeField(default=(datetime.now))


class Comit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comituser")
    comit = models.TextField()


class Lot(models.Model):
    lot_name = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = price = models.IntegerField()
    price = models.ManyToManyField(Bid, blank=True, related_name="lotbid")
    picture = models.URLField(blank=True)
    # category = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="lotcategory")
    userLot = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLot")
    user_comit = models.ManyToManyField(Comit, blank=True, related_name="usercomit")
    time_lot = models.DateTimeField(default=datetime.now)
    time_sales = models.DateTimeField(default=datetime.now)
    sale = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if datetime.now() >= self.time_sales:
    #         self.sale = True
    #     super(Lot, self).save(*args, **kwargs)