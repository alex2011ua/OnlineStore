from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"category", views.CategoryViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("guest_user/", include("my_apps.shop.api_v1.guest_user.guest_user_routes")),
    path("auth_user/", include("my_apps.shop.api_v1.auth_user.auth_user_routes")),
    path("manager/", include("my_apps.shop.api_v1.manager.manager_routes")),
    path("admin/", include("my_apps.shop.api_v1.admin.admin_routes")),
]
