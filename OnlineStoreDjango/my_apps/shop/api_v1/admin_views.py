from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from my_apps.shop.api_v1.serializers import ProductSerializer
from my_apps.shop.models import Product
from my_apps.shop.api_v1.permissions import AdminPermission

class TestAdmin(APIView):
    """Return product according to input price"""
    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})
