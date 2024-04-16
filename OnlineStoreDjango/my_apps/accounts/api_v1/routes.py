from django.urls import include, path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .guest_user_views import (
    GoogleAuth,
    GoogleAuthCode,
    GoogleAuthURL,
)
from .auth_user_views import (
    MyTokenObtainPairView,
)

#
# from django.contrib.auth.views import (
#
#     PasswordResetDoneView,
#     PasswordResetConfirmView,
#     PasswordResetCompleteView,
# )

urlpatterns = [

    path("guest_user/", include("my_apps.accounts.api_v1.guest_user_routes")),
    path("auth_user/", include("my_apps.accounts.api_v1.auth_user_routes")),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("google_auth_url/", GoogleAuthURL.as_view()),
    path("google_auth/", GoogleAuth.as_view()),
    path("google_auth_code/", GoogleAuthCode.as_view()),
    # path(
    #     "password-reset/",
    #     PasswordResetAPI.as_view(template_name="accounts/password_reset.html"),
    #     name="password-reset",
    # ),
    # path(
    #     "password-reset/done/",
    #     PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset-confirm/<uidb64>/<token>/",
    #     PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset-complete/",
    #     PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
    #     name="password_reset_complete",
    # ),
]
