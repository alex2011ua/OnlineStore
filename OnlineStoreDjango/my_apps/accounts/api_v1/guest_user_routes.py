from django.urls import path

from . import guest_user_views


urlpatterns = [
    path("create_auth_user/", guest_user_views.CreateUserView.as_view(), name="create_auth_user"),
    # path("reset_password/", guest_user_views.ResetPasswordView.as_view(), name="reset_password"),




]
