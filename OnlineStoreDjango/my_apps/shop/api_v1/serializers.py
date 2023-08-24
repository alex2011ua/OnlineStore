from rest_framework import serializers

from my_apps.shop.models import Category, Order, Product, Rating, Review, Banner


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
            "created_at",
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
        fields = ["id", "title", "description", "img", "link"]
