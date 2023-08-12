from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"category", views.CategoryViewSet)
router.register(r"product", views.ProductViewSet)
router.register(r"order", views.OrderViewSet)
router.register(r"review", views.ReviewViewSet)
router.register(r"rating", views.RatingViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("na/", include("my_apps.shop.api_v1.na_routes")),
]