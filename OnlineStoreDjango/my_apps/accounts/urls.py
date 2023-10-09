from django.urls import path
from . import views


urlpatterns = [
    path('', views.google_login),
    path("ok/", views.ok),

]