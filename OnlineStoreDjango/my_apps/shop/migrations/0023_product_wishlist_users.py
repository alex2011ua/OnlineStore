# Generated by Django 4.2.3 on 2023-09-13 10:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0022_remove_product_wishlist_users_delete_wishlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="wishlist_users",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
