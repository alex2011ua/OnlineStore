import json
from typing import Any

from django.utils.translation import get_language
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from my_apps.shop.models import Banner, BasketItem, Category, Faq, Order, Product, Review


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


class ProductCatalogSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_name")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "quantity",
            "img",
            "category",
            "price",
            "discount",
            "global_rating",
        ]


class ProductCardSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_name")
    code = serializers.CharField(source="slug")
    img = serializers.SerializerMethodField()
    # faq = serializers.CharField(source="get_faq_list")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "discount",
            "img",
            "quantity",
            "code",
            "global_rating",
            "description",
            # "faq",
            "rate_by_criteria",
            "rate_by_stars",
        ]

    def get_reviews(self, obj):
        serializer = ReviewSerializer(obj.get_reviews(), context=self.context, many=True)
        return serializer.data

    #
    # def get_faq(self, obj) -> str:
    #     list_faq: list = obj.get_list_faq()
    #     return json.dumps(list_faq)

    def get_img(self, obj):
        request = self.context.get("request")
        domain = request.build_absolute_uri("/")

        list_foto = obj.images()
        list_link = []
        for image in list_foto:
            list_link.append(domain + image)
        return list_link


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer", "manager", "status", "order_date", "total_amount"]

    status = serializers.CharField(source="get_status_display")


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["text", "rate_by_stars", "quality", "description_match", "photo_match", "price"]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="get_user_name")

    class Meta:
        model = Review
        fields = ["id", "author", "text", "rate_by_stars", "rate_by_criteria"]


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
