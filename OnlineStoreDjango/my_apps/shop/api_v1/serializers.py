from my_apps.shop.models import Category, Order, Product, Rating, Review
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "url",  "name", "slug", "description"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "url",
            "name",
            "image",
            "slug",
            "description",
            "category",
            "price",
            "discount",
            "quantity",
        ]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "url", "customer", "manager", "status", "order_date", "total_amount"]


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "url", "product", "customer", "title", "body", "created_at"]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "url", "product", "customer", "value", "created_at"]
