# Generated by Django 5.0 on 2023-12-14 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0041_review_description_match_review_photo_match_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="description_match",
            field=models.IntegerField(
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
                default=0,
                verbose_name="description match",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="photo_match",
            field=models.IntegerField(
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
                default=0,
                verbose_name="foto quality rating",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="price",
            field=models.IntegerField(
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
                default=0,
                verbose_name="price",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="quality",
            field=models.IntegerField(
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
                default=0,
                verbose_name="quality rating",
            ),
        ),
    ]
