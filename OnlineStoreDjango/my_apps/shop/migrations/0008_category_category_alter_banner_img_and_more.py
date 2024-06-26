# Generated by Django 4.2.3 on 2023-08-29 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0007_alter_banner_description_alter_banner_link_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sub_category",
                to="shop.category",
            ),
        ),
        migrations.AlterField(
            model_name="banner",
            name="img",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="foto/banners/",
                verbose_name="banner image",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="category description"),
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="category/",
                verbose_name="category image",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="image_small",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="category/",
                verbose_name="category icon image small",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                blank=True, null=True, unique=True, verbose_name="category slug"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="product/",
                verbose_name="product image",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image_small",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="product/",
                verbose_name="product image small",
            ),
        ),
    ]
