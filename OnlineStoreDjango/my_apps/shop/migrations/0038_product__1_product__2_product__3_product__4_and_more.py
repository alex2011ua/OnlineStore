# Generated by Django 4.2.3 on 2023-11-24 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0037_remove_product_delivery_remove_product_foto_quality_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="_1",
            field=models.IntegerField(blank=True, null=True, verbose_name="number of reviews 1*"),
        ),
        migrations.AddField(
            model_name="product",
            name="_2",
            field=models.IntegerField(blank=True, null=True, verbose_name="number of reviews 2*"),
        ),
        migrations.AddField(
            model_name="product",
            name="_3",
            field=models.IntegerField(blank=True, null=True, verbose_name="number of reviews 3*"),
        ),
        migrations.AddField(
            model_name="product",
            name="_4",
            field=models.IntegerField(blank=True, null=True, verbose_name="number of reviews 4*"),
        ),
        migrations.AddField(
            model_name="product",
            name="_5",
            field=models.IntegerField(blank=True, null=True, verbose_name="number of reviews 5*"),
        ),
        migrations.AlterField(
            model_name="rating",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]