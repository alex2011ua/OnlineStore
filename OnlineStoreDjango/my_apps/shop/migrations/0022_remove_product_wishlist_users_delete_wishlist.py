# Generated by Django 4.2.3 on 2023-09-13 10:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0021_product_wishlist_users"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="wishlist_users",
        ),
        migrations.DeleteModel(
            name="Wishlist",
        ),
    ]
