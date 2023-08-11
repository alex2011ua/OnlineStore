from rest_framework import serializers

from my_apps.shop.models import Category, Order, Product, Rating, Review


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "url",  "name", "slug", "description"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "slug",
            "description",
            "category",
            "price",
            "discount",
            "quantity",
            "sold",
            "global_rating",
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
