from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import jwt
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.conf import settings
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.viewsets import GenericViewSet

from my_apps.accounts.models import User
from django.contrib.auth.views import PasswordResetView
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from my_apps.shop.api_v1.permissions import AdminPermission, GuestUserPermission
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated

class MyTokenObtainPairView(TokenObtainPairView):
    """Custom clas for add user info in tocken response"""

    class TokenObtainPairResponseSerializer(serializers.Serializer):
        access = serializers.CharField()
        refresh = serializers.CharField()

        def create(self, validated_data):
            raise NotImplementedError()

        def update(self, instance, validated_data):
            raise NotImplementedError()

    @extend_schema(
        tags=["Accounts"],
        # responses={
        #     status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        # },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        access_token = response.data["access"]
        user = User.objects.get(email=request.data["email"])
        response.data["email"] = user.email
        response.data["role"] = user.get_role_display()
        response.data["user_id"] = user.id
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        return response


class ChangePasswordView(APIView):
    """
    API endpoint that allows to change user password.
    """

    class PasswordChangeSerializer(serializers.Serializer):
        current_password = serializers.CharField(style={"input_type": "password"}, required=True)
        new_password = serializers.CharField(style={"input_type": "password"}, required=True)

        def validate_current_password(self, value):
            if not self.context["request"].user.check_password(value):
                raise serializers.ValidationError({"current_password": "Does not match"})
            return value

    @extend_schema(
        tags=["Accounts"],
        request=PasswordChangeSerializer,
        responses={
            200: OpenApiResponse(),
            404: OpenApiResponse(description="detail"),
        },
    )
    def post(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated()

        def send_html_email(subject, html_message, recipient_list):
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                "your_email@example.com",  # Отправитель
                recipient_list,
                html_message=html_message,
            )

        serializer = self.PasswordChangeSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        payload = {"new_password": serializer.validated_data["new_password"], "email": user.email}
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        subject = "Password Change Confirmation"
        html_message = render_to_string(
            "accounts/email_change_pass.html",
            {"user": user, "jwt": encoded_jwt, "url_request": request.build_absolute_uri()},
        )
        recipient_list = [user.email]
        send_html_email(subject, html_message, recipient_list)

        return Response(status=status.HTTP_200_OK)

    @extend_schema(exclude=True)
    def get(self, request):
        encoded_jwt = request.query_params.get("jwt")
        try:
            payload = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return render(request, "accounts/error.html")
        user = User.objects.get(email=payload["email"])
        user.set_password(payload["new_password"])
        user.save()
        return render(request, "accounts/pass_changed.html")


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

    class UserUrlSerializer(serializers.ModelSerializer):
        class Meta:
            model = User

            fields = [
                "id",
                "url",
                "email",
                "first_name",
                "middle_name",
                "last_name",
                "address",
                "dob",
                "gender",
                "role",
                "notice",
                "get_age",
            ]

        gender = serializers.CharField(source="get_gender_display")
        role = serializers.CharField(source="get_role_display")

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserUrlSerializer
    permission_classes = [IsAuthenticated, AdminPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"detail": "Deleted", "code": "deleted"}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)


@extend_schema(tags=["Accounts"])
class CreateUserView(generics.CreateAPIView):
    """
    API endpoint that allows to create user.
    """

    permission_classes = [IsAuthenticated,
                          # GuestUserPermission
                          ]

    class RegistrationSerializer(serializers.ModelSerializer):
        role = serializers.CharField(source="get_role_display")

        def validate_role(self, value):
            ROLE_CHOICES = {
                "admin": "A",
                "manager": "M",
                "auth_user": "U",
            }
            if value in ROLE_CHOICES:
                return ROLE_CHOICES[value]
            else:
                raise serializers.ValidationError({"detail": "wrong role field"})

        class Meta:
            model = User
            fields = ["email", "password", "role"]
            extra_kwargs = {"password": {"write_only": True}}

        def save(self):
            user = User(
                email=self.validated_data["email"],
                role=self.validated_data["get_role_display"],
            )
            password = self.validated_data["password"]

            user.set_password(password)
            user.save()
            return user

    @extend_schema(tags=["Accounts"],
                   request=RegistrationSerializer())
    def post(self, request):
        serializer = self.RegistrationSerializer(data=request.data)
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
            "auth_user": [],
            "manager": ["auth_user"],
            "admin": ["auth_user", "manager", "admin"],
        }
        if request.data["role"] in rules[request.user.get_role_display()]:
            return

        return True
