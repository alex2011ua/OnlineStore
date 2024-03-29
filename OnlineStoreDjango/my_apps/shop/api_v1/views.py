from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response

from my_apps.shop.models import Category, Product, Review

from .serializers import (
    CategorySerializer,
    ReviewSerializer,
)


class MyDestroyModelMixin(DestroyModelMixin):
    """Add additional info in response when instance deleted"""

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"detail": "Deleted", "code": "deleted"}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)


@extend_schema(exclude=True)
class CategoryViewSet(viewsets.ModelViewSet, MyDestroyModelMixin):
    """
    API endpoint that allows made CRUD operations with Category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(exclude=True)
class ReviewViewSet(viewsets.ModelViewSet, MyDestroyModelMixin):
    """
    API endpoint that allows made CRUD operations with users reviews.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
