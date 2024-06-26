# Generated by Django 5.0 on 2024-02-24 09:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0051_alter_order_delivery_option_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("new_order", "new order"),
                    ("ready", "ready"),
                    ("on_its_way", "on its way"),
                    ("delivered", "delivered"),
                ],
                default="new_order",
                max_length=11,
            ),
        ),
    ]
