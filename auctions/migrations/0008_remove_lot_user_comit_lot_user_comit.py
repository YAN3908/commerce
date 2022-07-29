# Generated by Django 4.0.5 on 2022-07-28 21:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_lot_price_lot_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='user_comit',
        ),
        migrations.AddField(
            model_name='lot',
            name='user_comit',
            field=models.ManyToManyField(blank=True, related_name='usercomit', to=settings.AUTH_USER_MODEL),
        ),
    ]
