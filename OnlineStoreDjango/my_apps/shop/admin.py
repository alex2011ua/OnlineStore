from django.contrib import admin
from my_apps.shop.models import (Banner, Category, Order, OrderItem, Product,
                                 Rating, Review)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "slug",
        "description",
        "created_at",
        "updated_at",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "type",
        "category",
        "price",
        "img",
        "discount",
        "quantity",
        "sold",
        "global_rating",
        "created_at",
        "updated_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
    )


@admin.register(Review)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "customer",
        "title",
        "body",
        "created_at",
        "updated_at",
    )

@admin.register(Banner)
class RatingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "img", "link")
