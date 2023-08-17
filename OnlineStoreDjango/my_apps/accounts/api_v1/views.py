from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from my_apps.accounts.models import User
from my_apps.shop.api_v1.permissions import AdminPermission, GuestUserPermission
from .serializers import (
    MyTokenObtainPairSerializer,
    PasswordChangeSerializer,
    RegistrationSerializer,
    UserUrlSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom clas for add user info in tocken response"""

    serializer_class = MyTokenObtainPairSerializer

@extend_schema(tags=["User"])
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows users to be viewed.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserUrlSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"detail": "Deleted", "code": "deleted"}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)


@extend_schema(tags=["User"])
class CreateUserView(generics.CreateAPIView):
    """
    API endpoint that allows to create user.
    """

    permission_classes = [IsAuthenticated, GuestUserPermission]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if self.validate_roles(request):
                return Response(
                    {"detail": "this user can't create another user with this role"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer.save()
            user = User.objects.get(email=serializer.data["email"])
            data = serializer.data
            data["id"] = user.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def validate_roles(request):
        """
        Describe what user can create other user with role.
        Like "manager" can create only "auth_user"
        """
        rules = {
            "guest_user": ["auth_user"],
            "auth_user": [],
            "manager": ["auth_user"],
            "admin": ["auth_user", "manager", "admin"],
        }
        if request.data["role"] in rules[request.user.get_role_display()]:
            return

        return True


@extend_schema(tags=["User"])
class ChangePasswordView(APIView):
    """
    API endpoint that allows to change user password.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
