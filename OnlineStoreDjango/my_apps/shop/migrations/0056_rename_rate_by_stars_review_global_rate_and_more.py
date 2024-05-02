# Generated by Django 5.0 on 2024-05-02 10:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0055_alter_order_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="rate_by_stars",
            new_name="global_rate",
        ),
        migrations.AlterField(
            model_name="product",
            name="description_match",
            field=models.IntegerField(
                choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                default=0,
                verbose_name="description_match",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="photo_match",
            field=models.IntegerField(
                choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                default=0,
                verbose_name="photo_match",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="quality",
            field=models.IntegerField(
                choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                default=0,
                verbose_name="quality rating",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="rating_price",
            field=models.IntegerField(
                choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                default=0,
                verbose_name="price",
            ),
        ),
    ]
