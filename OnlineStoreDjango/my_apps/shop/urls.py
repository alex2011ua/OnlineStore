from django.urls import path

from .views import get_foto_product, get_foto_banner

urlpatterns = [
    path("products/<str:image_path>/", get_foto_product),
    path("banners/<str:image_path>/", get_foto_banner),
]
