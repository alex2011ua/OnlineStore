from django.urls import path, include

from . import guest_user_views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'product', guest_user_views.GetProduct, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path("search/", guest_user_views.ListSearchGifts.as_view(), name="search"),
    path("gpt/", guest_user_views.Gpt.as_view(), name="gpt"),
    path("random-gifts/", guest_user_views.ListRandomGifts.as_view(), name="random_gifts"),
    path("banner_list/", guest_user_views.ListBanners.as_view(), name="banner_list"),
    path(
        "get_all_categories/",
        guest_user_views.GetAllCategories.as_view({"get": "list"}),
        name="get_all_categories",
    ),
    path(
        "category/<category_id>/products",
        guest_user_views.GetProductsByCategory.as_view({"get": "list"}),
        name="get_products_by_category",
    ),
    path(
        "category/url/<url_category>/",
        guest_user_views.get_category_by_slug,
        name="get_category_by_slug",
    ),

    path(
        "product/<prod_pk>/comments",
        guest_user_views.Comments.as_view({"get": "list"}),
        name="get_product_comments",
    ),
    path("store_info/", guest_user_views.store_info, name="store_info"),
    path("order_create/", guest_user_views.OrderCreate.as_view(), name="order_create"),

]
