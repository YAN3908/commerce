# Generated by Django 4.0.5 on 2022-07-28 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_lot_user_comit_alter_bid_user_alter_lot_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='user_comit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usercomit', to=settings.AUTH_USER_MODEL),
        ),
    ]
