# Generated by Django 4.2.3 on 2023-11-18 00:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0034_remove_banner_img_en_remove_banner_img_ua_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="banner",
            name="img_en",
            field=models.ImageField(
                blank=True, null=True, upload_to="foto/banners/", verbose_name="banner image"
            ),
        ),
        migrations.AddField(
            model_name="banner",
            name="img_ua",
            field=models.ImageField(
                blank=True, null=True, upload_to="foto/banners/", verbose_name="banner image"
            ),
        ),
        migrations.AddField(
            model_name="banner",
            name="mobileImg_en",
            field=models.ImageField(
                blank=True, null=True, upload_to="foto/banners/", verbose_name="banner for mobile"
            ),
        ),
        migrations.AddField(
            model_name="banner",
            name="mobileImg_ua",
            field=models.ImageField(
                blank=True, null=True, upload_to="foto/banners/", verbose_name="banner for mobile"
            ),
        ),
    ]
