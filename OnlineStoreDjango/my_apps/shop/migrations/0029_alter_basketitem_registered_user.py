# Generated by Django 4.2.3 on 2023-10-13 17:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0028_basketitem_product_valid_price_basketitem_product_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basketitem",
            name="registered_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="basket",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]