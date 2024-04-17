from django.urls import include, path
from rest_framework import routers
from .admin_user_views import (
    UserViewSet,
)
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path("", include(router.urls)),

]
