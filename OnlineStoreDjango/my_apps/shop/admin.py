from django.contrib import admin
from my_apps.shop.models import (
    Banner,
    Category,
    Order,
    OrderItem,
    Product,
    Rating,
    Review,
    BasketItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "slug",
        "img_small",
        "img",
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


@admin.register(Banner)
class BanerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "img",
        "mobileImg",
        "link",
        "created_at",
        "updated_at",
        "title",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "customer",
        "title",
        "body",
        "created_at",
        "updated_at",
    )


@admin.register(BasketItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "registered_user",
        "product",
        "quantity",
    )
