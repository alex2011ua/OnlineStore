from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from my_apps.shop.models import Banner, Category, Product, Review


class ProductIdSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def validate_id(self, value):
        """
        Check that id valid.
        """
        try:
            Product.objects.get(id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Product with this ID not exist")
        return value


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
