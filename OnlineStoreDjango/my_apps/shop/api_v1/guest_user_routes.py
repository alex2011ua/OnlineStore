from django.urls import path

from . import guest_user_views

urlpatterns = [
    path("test/", guest_user_views.TestGuestUser.as_view()),
    path("search/", guest_user_views.ListSearchGifts.as_view(), name="search"),
    path("gpt/", guest_user_views.Gpt.as_view(), name="gpt"),
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
        "category/url/<url_category>/",
        guest_user_views.get_category_by_slug,
        name="get_category_by_slug",
    ),
    path(
        "product/<pk>",
        guest_user_views.GetProduct.as_view(),
        name="get_product",
    ),
    path(
        "product/<prod_pk>/comments",
        guest_user_views.Comments.as_view({'get': 'list'}),
        name="get_product_comments",
    ),
    path(
        "product/<prod_pk>/comments/<pk>",
        guest_user_views.Comments.as_view({'get': 'retrieve'}),
        name="get_product_comment",
    ),
    path("store_info/", guest_user_views.store_info, name="store_info"),
]
