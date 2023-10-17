from django.urls import path

from . import guest_user_views

urlpatterns = [
    path("test/", guest_user_views.TestGuestUser.as_view()),
    path("popular/", guest_user_views.ListPopularGifts.as_view(), name="list_popular"),
    path("search/", guest_user_views.ListSearchGifts.as_view(), name="search"),
    path("gpt/", guest_user_views.Gpt.as_view(), name="gpt"),
    path(
        "new-products/",
        guest_user_views.ListNewGifts.as_view(),
        name="list_new_products",
    ),
    path("random-gift/", guest_user_views.RandomGift.as_view(), name="random_gift"),
    path(
        "random-gifts/", guest_user_views.ListRandomGifts.as_view(), name="random_gifts"
    ),
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
        "product/<product_id>",
        guest_user_views.GetProduct.as_view({"get": "retrieve"}),
        name="get_product",
    ),
]
