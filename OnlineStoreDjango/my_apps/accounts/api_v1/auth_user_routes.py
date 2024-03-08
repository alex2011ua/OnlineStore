from django.urls import include, path
from rest_framework import routers
from .auth_user_views import (
    ChangePasswordView,
    CreateUserView,
    UserViewSet,
)
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path("", include(router.urls)),
    path("user-create/", CreateUserView.as_view(), name="create_user"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
