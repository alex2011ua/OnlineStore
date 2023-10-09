from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (ChangePasswordView, CreateUserView, MyTokenObtainPairView,
                    UserViewSet, GoogleAuth, GoogleMail)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user-create/", CreateUserView.as_view(), name="create_user"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("guest_user/", include("my_apps.accounts.api_v1.guest_user_routes")),
    path("google_auth/", GoogleAuth.as_view()),
    path("google_mail/", GoogleMail.as_view()),
]
