# Generated by Django 4.0.5 on 2022-07-28 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bidd_category_lot'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bidd',
            new_name='Bid',
        ),
    ]
