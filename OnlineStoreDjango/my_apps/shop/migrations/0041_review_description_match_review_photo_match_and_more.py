# Generated by Django 5.0 on 2023-12-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0040_rename_customer_review_author_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="description_match",
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
                verbose_name="description match",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="photo_match",
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
        migrations.AddField(
            model_name="review",
            name="price",
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
                verbose_name="price",
            ),
        ),
        migrations.AddField(
            model_name="review",
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
        migrations.AddField(
            model_name="review",
            name="rate_by_stars",
            field=models.IntegerField(
                choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                default=0,
                verbose_name="rate by stars",
            ),
        ),
        migrations.DeleteModel(
            name="Rating",
        ),
    ]
