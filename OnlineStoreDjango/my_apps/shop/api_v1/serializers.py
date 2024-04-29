import json
from typing import Any

from django.utils.translation import get_language
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from my_apps.shop.models import Banner, BasketItem, Category, Faq, Product, Review


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
    isInCart = serializers.SerializerMethodField()
    isInWishlist = serializers.SerializerMethodField()

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
            "isInCart",
            "isInWishlist",
        ]

    def get_isInCart(self, obj):
        return obj.is_in_cart(self.context["request"].user)

    def get_isInWishlist(self, obj):
        return obj.is_in_wishlist(self.context["request"].user)


class AuthProductCatalogSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_name")
    isInCart = serializers.SerializerMethodField()
    isInWishlist = serializers.SerializerMethodField()

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
            "isInCart",
            "isInWishlist",
        ]

    def get_isInCart(self, obj):
        return True if obj in self.context["products"] else False

    def get_isInWishlist(self, obj):
        return True if obj in self.context["wishlist"] else False


class ProductCardSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_name")
    code = serializers.CharField(source="slug")
    img = serializers.SerializerMethodField()
    isInCart = serializers.SerializerMethodField()
    isInWishlist = serializers.SerializerMethodField()
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
            "isInCart",
            "isInWishlist",
        ]

    def get_isInCart(self, obj):
        return obj.is_in_cart(self.context["request"].user)

    def get_isInWishlist(self, obj):
        return obj.is_in_wishlist(self.context["request"].user)

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
    isSecretPresent = serializers.BooleanField(default=False, required=False)


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ["product", "quantity"]


class OrderIdSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
