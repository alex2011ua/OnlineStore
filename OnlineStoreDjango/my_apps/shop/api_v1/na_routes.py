from django.urls import path

from . import na_views

urlpatterns = [
    path("popular/", na_views.ListPopularGifts.as_view(), name="list_popular"),

]
