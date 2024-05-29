# Generated by Django 4.2.3 on 2023-10-01 20:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0026_alter_order_customer"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["created_at", "price"], name="shop_produc_created_3b0d54_idx"
            ),
        ),
    ]