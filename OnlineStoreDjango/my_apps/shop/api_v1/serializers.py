from typing import Any

from django.utils.translation import get_language
from rest_framework.utils.serializer_helpers import ReturnDict

from my_apps.shop.models import (
    Banner,
    BasketItem,
    Category,
    Order,
    Product,
    Rating,
    Review,
)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    sub = serializers.SerializerMethodField()
    icon = serializers.ImageField(source="img_small")
    url = serializers.CharField(source="slug")

    class Meta:
        model = Category
        fields = [
            "id",
            "url",
            "name",
            "icon",
            "img",
            "sub",
        ]

    def get_sub(self, obj) -> ReturnDict[Any, Any]:
        serializer = CategorySerializer(obj.get_sub_categories(), context=self.context, many=True)
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_name")
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "type",
            "description",
            "quantity",
            "sold",
            "img",
            "category",
            "price",
            "discount",
            "global_rating",
            "reviews",
        ]

    def get_reviews(self, obj):
        serializer = ReviewSerializer(obj.get_rewievs(), context=self.context, many=True)
        return serializer.data


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer", "manager", "status", "order_date", "total_amount"]

    status = serializers.CharField(source="get_status_display")


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "title", "body", "created_at"]

    def save(self, owner, product):
        title = self.validated_data["title"]
        body = self.validated_data["body"]
        rewiev = Review(title=title, body=body, customer=owner, product=product)
        rewiev.save()
        return rewiev


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="get_user_name")

    class Meta:
        model = Review
        fields = ["id", "user_name", "title", "body", "created_at"]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "url", "product", "customer", "value", "created_at"]


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ["id", "img", "mobileImg", "link"]


class BasketSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    amount = serializers.IntegerField()


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ["product", "quantity"]


class OrderIdSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
