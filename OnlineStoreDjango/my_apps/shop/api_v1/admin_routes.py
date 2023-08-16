from django.urls import path

from . import admin_views

urlpatterns = [
    path("test/", admin_views.TestAdmin.as_view()),
]