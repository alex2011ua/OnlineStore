from django.urls import include, path
from rest_framework import routers

from my_apps.shop.api_v1.admin import admin_views

router = routers.DefaultRouter()
router.register(r"banner", admin_views.BannerViewSet)

urlpatterns = [
    path("test/", admin_views.TestAdmin.as_view()),
    path("", include(router.urls)),
]
