from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from my_apps.shop.api_v1.permissions import ManagerPermission


@extend_schema(tags=["Manager"])
class TestManager(APIView):
    """Return product according to input price"""

    permission_classes = [IsAuthenticated, ManagerPermission]

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})
