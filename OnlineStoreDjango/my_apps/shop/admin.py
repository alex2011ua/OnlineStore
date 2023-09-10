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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "customer",
        "manager",
        "order_date",
        "updated_at",
        "total_amount",
    )
    raw_id_fields = ("products",)


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


@admin.register(Rating)
class RatingItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "customer",
        "global_value",
        "quality",
        "delivery",
        "foto_quality",
        "description_quality",
        "value",
        "created_at",
        "updated_at",
    )


@admin.register(Banner)
class RatingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "img", "link")
