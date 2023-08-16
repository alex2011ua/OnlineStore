from django.urls import path

from . import auth_user_views

urlpatterns = [
    path("test/", auth_user_views.TestAuthUser.as_view()),

]
