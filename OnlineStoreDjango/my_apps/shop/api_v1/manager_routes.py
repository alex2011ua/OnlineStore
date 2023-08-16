from django.urls import path

from . import manager_views

urlpatterns = [
    path("test/", manager_views.TestManager.as_view())
]