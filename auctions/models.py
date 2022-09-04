from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class User(AbstractUser):
    # userLot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="userLot")
    pass


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category.title()} "


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biduser")
    price = models.IntegerField()
    time_lot = models.DateTimeField(default=(datetime.now))

    def __str__(self):
        return f"{self.user}({self.price}$)"


class Comit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comituser")
    comit = models.TextField()

    def __str__(self):
        return f"{self.user} "


class Imagetab(models.Model):
    urlimage = models.URLField(max_length=512, blank=True)
    uploadimage = models.ImageField(upload_to="images/", blank=True, default=None)


@receiver(pre_delete, sender=Imagetab)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.uploadimage.delete(False)


class Lot(models.Model):
    lot_name = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = price = models.IntegerField()
    price = models.ManyToManyField(Bid, blank=True, related_name="lotbid")
    picture = models.URLField(blank=True)
    image = models.ManyToManyField(Imagetab, blank=True, related_name="lotimage")
    # category = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="lotcategory")
    userLot = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLot")
    user_comit = models.ManyToManyField(Comit, blank=True, related_name="usercomit")
    time_lot = models.DateTimeField(default=datetime.now)
    time_sales = models.DateTimeField(default=datetime(1, 1, 1, 0, 0))
    sale = models.BooleanField(default=False)  # not used
    # class Meta:
    #     Verbose_name = 'Лоты'

    # def save(self, *args, **kwargs):
    #     if datetime.now() >= self.time_sales:
    #         self.sale = True
    #     super(Lot, self).save(*args, **kwargs)
