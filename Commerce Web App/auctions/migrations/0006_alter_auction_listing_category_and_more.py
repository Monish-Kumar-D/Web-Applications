# Generated by Django 5.0.1 on 2024-06-13 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_remove_auction_listing_starting_bid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction_listing",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="item_category",
                to="auctions.category",
            ),
        ),
        migrations.AlterField(
            model_name="auction_listing",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="auction_listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="watchlist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="bids",
            name="user_name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="User",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="comments",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listitem",
                to="auctions.auction_listing",
            ),
        ),
        migrations.AlterField(
            model_name="comments",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commenter",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
