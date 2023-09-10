from django.urls import path

from . import auth_user_views

urlpatterns = [
    path("test/", auth_user_views.TestAuthUser.as_view()),
    path(
        "add_product_to_order/",
        auth_user_views.AddProductOrder.as_view(),
        name="add_product_to_order",
    ),
]
