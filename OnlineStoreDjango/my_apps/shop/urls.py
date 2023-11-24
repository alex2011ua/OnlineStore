from django.urls import path

from .views import get_foto_banner, get_foto_category, get_foto_product, gpt_search

urlpatterns = [
    path("products/<str:image_path>/", get_foto_product),
    path("banners/<str:image_path>/", get_foto_banner),
    path("categories/<str:image_path>/", get_foto_category, name="get_categories_foto"),
    path("gpt/", gpt_search, name="gpt"),
]
