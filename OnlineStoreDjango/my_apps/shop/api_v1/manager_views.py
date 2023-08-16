from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from my_apps.shop.api_v1.serializers import ProductSerializer
from my_apps.shop.models import Product
from my_apps.shop.api_v1.permissions import ManagerPermission


class TestManager(APIView):
    """Return product according to input price"""
    permission_classes = [IsAuthenticated, ManagerPermission]

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})
