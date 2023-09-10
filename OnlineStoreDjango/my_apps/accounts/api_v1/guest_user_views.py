from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from my_apps.accounts.models import User
from my_apps.shop.api_v1.permissions import AdminPermission, GuestUserPermission
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from .serializers import RegisterAuthUser


@extend_schema()
@extend_schema(
    tags=["Guest_user"],
    request=RegisterAuthUser,
    responses=RegisterAuthUser,
    # more customizations
)
class CreateUserView(APIView):
    """
    API endpoint that allows to create auth_user.
    """

    def post(self, request):
        serializer = RegisterAuthUser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data["email"])
            data = serializer.data
            data["id"] = user.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
