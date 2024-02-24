from django.urls import path

from .views import get_foto_banner, get_foto_category, get_foto_product

urlpatterns = [
    path("products/<str:image_path>/", get_foto_product),
    path("banners/<path:image_path>", get_foto_banner),
    path("categories/<str:image_path>/", get_foto_category, name="get_categories_foto"),
    # path("gpt/", gpt_search, name="gpt"),
]
