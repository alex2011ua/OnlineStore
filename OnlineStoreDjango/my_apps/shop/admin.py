from django.contrib import admin

from my_apps.shop.models import (
    Banner,
    BasketItem,
    Category,
    Faq,
    Order,
    OrderItem,
    Product,
    Rating,
    Review,
    Settings,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "slug",
        "img_small",
        "img",
        "description",
        "created_at",
        "updated_at",
        "id",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "type",
        "category",
        "price",
        "img",
        "img1",
        "img2",
        "img3",
        "discount",
        "quantity",
        "sold",
        "global_rating",
        "quality",
        "price",
        "photo_match",
        "description_match",
        "created_at",
        "updated_at",
        "id",
    )
    list_filter = ("category", "price")
    ordering = ["name"]


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
        "author",
        "text",
        "date",
        "id",
    )
    list_filter = ("product", "author", "date")
    ordering = ["-date"]

@admin.register(BasketItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "registered_user",
        "product",
        "quantity",
    )


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "value",
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "customer",
        "rate_by_stars",
        "quality",
        "price",
        "photo_match",
        "description_match",
        "created_at",
        "updated_at",
    )


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer")
