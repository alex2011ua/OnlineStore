from django.urls import path
from my_apps.shop.api_v1.auth_user import auth_user_views

urlpatterns = [
    path("test/", auth_user_views.TestAuthUser.as_view()),
    path(
        "add_product_to_order/",
        auth_user_views.AddProductOrder.as_view(),
        name="add_product_to_order",
    ),
    path("wishlist/", auth_user_views.Wishlist.as_view(), name="add_del_wish_product"),
]
