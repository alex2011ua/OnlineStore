# Generated by Django 5.0 on 2024-01-23 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0044_order_address_order_another_person_firstname_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basketitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prod_in_basket",
                to="shop.product",
            ),
        ),
    ]
