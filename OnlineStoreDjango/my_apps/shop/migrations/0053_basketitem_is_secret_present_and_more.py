# Generated by Django 5.0 on 2024-03-14 21:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0052_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="basketitem",
            name="is_secret_present",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="is_secret_present",
            field=models.BooleanField(default=False),
        ),
    ]
