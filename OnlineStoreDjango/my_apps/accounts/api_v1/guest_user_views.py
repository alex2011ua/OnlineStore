from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from my_apps.accounts.models import User
from my_apps.shop.api_v1.permissions import AdminPermission, GuestUserPermission
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .responses_serializers import RegisterAuthUserWithToken
from .serializers import RegisterAuthUser


@extend_schema(
    tags=["Guest_user"],
    request=RegisterAuthUser,
    responses=RegisterAuthUserWithToken,
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
            refresh = RefreshToken.for_user(user)
            data["access"] = str(refresh.access_token)
            data["refresh"] = str(refresh)

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

