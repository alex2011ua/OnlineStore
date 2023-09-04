from my_apps.shop.models import (Banner, Category, Order, Product, Rating,
                                 Review)
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category", "url",  "name", "slug", "description", "img_small", "img"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_name")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "img",
            "category",
            "price",
            "discount",
            "global_rating",

        ]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "url", "customer", "manager", "status", "order_date", "total_amount"]
    status = serializers.CharField(source="get_status_display")


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "url", "product", "customer", "title", "body", "created_at"]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "url", "product", "customer", "value", "created_at"]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["id", "title", "description", "img", "mobileImg", "link"]
