from django.urls import path

from . import na_views

urlpatterns = [
    path("popular/", na_views.ListPopularGifts.as_view(), name="list_popular"),
    path("search/", na_views.ListSearchGifts.as_view(), name="search"),
    path("new-products/", na_views.ListNewGifts.as_view(), name="list_new_products"),
    path("random-gift/", na_views.RandomGift.as_view(), name="random_gift"),

]
