# Generated by Django 4.2.3 on 2023-08-10 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="delivery",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                ],
                null=True,
                verbose_name="delivery rating",
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="description_quality",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                ],
                null=True,
                verbose_name="description quality",
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="foto_quality",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                ],
                null=True,
                verbose_name="foto quality rating",
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="quality",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                ],
                null=True,
                verbose_name="quality rating",
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="value",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                ],
                null=True,
                verbose_name="another rating",
            ),
        ),
    ]
