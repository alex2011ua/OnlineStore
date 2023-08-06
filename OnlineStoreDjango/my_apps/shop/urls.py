from django.urls import path
from .views import get_foto
urlpatterns = [
    path('<str:image_path>/', get_foto),
    ]