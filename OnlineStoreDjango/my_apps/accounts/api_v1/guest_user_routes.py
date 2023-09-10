from django.urls import path

from . import guest_user_views

urlpatterns = [
    path("create_auth_user/", guest_user_views.CreateUserView.as_view(), name="create_auth_user"),


]
