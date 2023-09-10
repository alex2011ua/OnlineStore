from django.urls import include, path
from my_apps.shop.models import Banner
from rest_framework import routers

from . import admin_views
from .serializers import BannerSerializer

router = routers.DefaultRouter()
router.register(r"banner", admin_views.BannerViewSet)

urlpatterns = [
    path("test/", admin_views.TestAdmin.as_view()),
    path("", include(router.urls)),
]
