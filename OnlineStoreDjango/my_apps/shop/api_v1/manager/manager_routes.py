from django.urls import path

from my_apps.shop.api_v1.manager import manager_views

urlpatterns = [path("test/", manager_views.TestManager.as_view())]
