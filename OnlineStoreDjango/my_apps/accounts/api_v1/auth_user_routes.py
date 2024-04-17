from django.urls import include, path

from .auth_user_views import (
    ChangePasswordView,
    CreateUserView,
    GetAuthUserInfo
)


urlpatterns = [
    path("user-create/", CreateUserView.as_view(), name="create_user"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("user_info/", GetAuthUserInfo.as_view(), name="auth_user_info"),
]
