from my_apps.shop.models import Product, Category, Order, Review, Rating
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'slug', 'description']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'name', 'slug', 'description', "category", "price", "discount", "quantity"]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'customer', "manager", "status", 'order_date', 'total_amount']


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ['url', 'product', 'customer',  'title', "body", "created_at"]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ['url', 'product', 'customer', 'value', "created_at"]

