from drf_spectacular.utils import extend_schema, extend_schema_view
from my_apps.shop.api_v1.permissions import AdminPermission
from my_apps.shop.api_v1.serializers import BannerSerializer, ProductSerializer
from my_apps.shop.models import Banner, Product
from rest_framework import status, viewsets
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MyDestroyModelMixin(DestroyModelMixin):
    """Add additional info in response when instance deleted"""

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"detail": "Deleted", "code": "deleted"}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)


@extend_schema(tags=["Admin user"])
class TestAdmin(APIView):
    """Just endpoint for test admin permissions"""

    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})


@extend_schema(tags=["Admin user"])
@extend_schema_view(
    list=extend_schema(
        summary="Get list banners",
        request=BannerSerializer,
    ),
    update=extend_schema(summary="update banner", request=BannerSerializer),
    create=extend_schema(
        summary="Create new banner",
        request=BannerSerializer,
    ),
)
class BannerViewSet(viewsets.ModelViewSet, MyDestroyModelMixin):
    """API endpoint that allows made CRUD operations with Banner."""

    pagination_class = None
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticated, AdminPermission]
