from django.urls import path

from my_apps.shop.api_v1.auth_user import auth_user_views

urlpatterns = [
    path("test/", auth_user_views.TestAuthUser.as_view()),
    path("basket/", auth_user_views.Basket.as_view(), name="auth_user_basket"),
    path("basket/clear/", auth_user_views.BasketClear.as_view(), name="auth_user_basket_clear"),
    path("wishlist/", auth_user_views.Wishlist.as_view(), name="wishlist"),
    path("wishlist/del_list_products/", auth_user_views.DelListProducts.as_view(), name="wishlist_del_list_products"),
    path(
        "product/<pk>/comments",
        auth_user_views.AuthComments.as_view(),
        name="auth_comments",
    ),
]
