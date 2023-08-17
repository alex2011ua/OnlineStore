from django.urls import path, include

from . import admin_views
from my_apps.shop.models import Banner
from .serializers import BannerSerializer
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"banner", admin_views.BannerViewSet)

urlpatterns = [
    path("test/", admin_views.TestAdmin.as_view()),
    path("", include(router.urls)),

]