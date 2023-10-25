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

    def get_sub(self, obj) -> list[dict]:
        serializer = CategorySerializer(
            obj.get_sub_categories(), context=self.context, many=True
        )
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_name")

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
        ]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer", "manager", "status", "order_date", "total_amount"]

    status = serializers.CharField(source="get_status_display")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "product", "customer", "title", "body", "created_at"]

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     valid = validated_data.copy()
    #     valid["customer"] = user.id
    #
    #     return Review(validated_data)

class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "url", "product", "customer", "value", "created_at"]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["id", "title", "description", "img", "mobileImg", "link"]


class BasketSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    amount = serializers.IntegerField()


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ["product", "quantity"]


class OrderIdSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
