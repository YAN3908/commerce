# Generated by Django 4.0.5 on 2022-07-28 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_lot_user_comit'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='starting_price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lot',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lotbid', to='auctions.bid'),
        ),
    ]
