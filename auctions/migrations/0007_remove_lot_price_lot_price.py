# Generated by Django 4.0.5 on 2022-07-28 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_lot_starting_price_alter_lot_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='price',
        ),
        migrations.AddField(
            model_name='lot',
            name='price',
            field=models.ManyToManyField(blank=True, related_name='lotbid', to='auctions.bid'),
        ),
    ]
