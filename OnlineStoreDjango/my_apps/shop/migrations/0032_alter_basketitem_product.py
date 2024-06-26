# Generated by Django 4.2.3 on 2023-11-11 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0031_settings_description_en_settings_description_ua_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basketitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prod_in_basket",
                to="shop.product",
                unique=True,
            ),
        ),
    ]
