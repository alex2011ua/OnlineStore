from django.urls import path

from . import guest_user_views

urlpatterns = [
    path("test/", guest_user_views.TestGuestUser.as_view()),
    path("popular/", guest_user_views.ListPopularGifts.as_view(), name="list_popular"),
    path("search/", guest_user_views.ListSearchGifts.as_view(), name="search"),
    path("new-products/", guest_user_views.ListNewGifts.as_view(), name="list_new_products"),
    path("random-gift/", guest_user_views.RandomGift.as_view(), name="random_gift"),
    path("random-gifts/", guest_user_views.ListRandomGifts.as_view(), name="random_gifts"),
    path("banner_list/", guest_user_views.ListBanners.as_view(), name="banner_list"),


]
