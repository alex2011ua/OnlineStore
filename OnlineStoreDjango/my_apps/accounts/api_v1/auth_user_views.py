from typing import Any

import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import generics, mixins, serializers, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from my_apps.accounts.models import User
from my_apps.shop.api_v1.permissions import AdminPermission, AuthUserPermission, GuestUserPermission
from .services import get_user_order_history
from ...shop.models import Order, Product, OrderItem


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


@extend_schema(tags=["Accounts"])
class CreateUserView(generics.CreateAPIView):
    """
    API endpoint that allows to create user.
    """

    permission_classes = [
        IsAuthenticated,
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

    @extend_schema(tags=["Accounts"], request=RegistrationSerializer())
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


@extend_schema(tags=["Auth_user"])
class GetAuthUserInfo(APIView):
    permission_classes = [IsAuthenticated, AuthUserPermission]

    class UserSerializer(serializers.ModelSerializer):
        class UkrPostaSerializer(serializers.Serializer):
            class Meta:
                model = User
                fields = ["town", "postOffice"]

            town = serializers.CharField(
                source="ukr_poshta_town",
            )
            postOffice = serializers.CharField(source="ukr_poshta_post_office")

            def update(self, instance, validated_data):
                instance.ukr_poshta_post_office = validated_data.get(
                    "ukr_poshta_post_office", instance.ukr_poshta_post_office
                )
                instance.ukr_poshta_town = validated_data.get(
                    "ukr_poshta_town", instance.ukr_poshta_town
                )
                instance.save()
                return instance

        class NovaPoshtaSerializer(serializers.Serializer):
            class Meta:
                model = User
                fields = ["town", "postOffice"]

            town = serializers.CharField(source="nova_poshta_town")
            postOffice = serializers.CharField(source="nova_poshta_post_office")

            def update(self, instance, validated_data):
                instance.nova_poshta_town = validated_data.get(
                    "nova_poshta_town", instance.nova_poshta_town
                )
                instance.nova_poshta_post_office = validated_data.get(
                    "nova_poshta_post_office", instance.nova_poshta_post_office
                )
                instance.save()
                return instance

        class AddressSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = [
                    "town",
                    "street",
                    "building",
                    "flat",
                ]

            town = serializers.CharField(source="address_town")
            street = serializers.CharField(source="address_street")
            building = serializers.CharField(source="address_building")
            flat = serializers.CharField(source="address_flat")

            def update(self, instance, validated_data):
                instance.address_town = validated_data.get("address_town", instance.address_town)
                instance.address_street = validated_data.get(
                    "address_street", instance.address_street
                )
                instance.address_building = validated_data.get(
                    "address_building", instance.address_building
                )
                instance.address_flat = validated_data.get("address_flat", instance.address_flat)
                instance.save()
                return instance

        novaPoshta = serializers.SerializerMethodField()
        ukrPoshta = serializers.SerializerMethodField()
        address = serializers.SerializerMethodField()
        gender = serializers.CharField(source="get_gender_display")
        role = serializers.CharField(source="get_role_display")

        class Meta:
            model = User
            fields = [
                "email",
                "first_name",
                "last_name",
                "mobile",
                "dob",
                "address",
                "novaPoshta",
                "ukrPoshta",
                "gender",
                "role",
                "notice",
                "get_age",
            ]

        def get_novaPoshta(self, obj) -> ReturnDict[Any, Any]:
            serializer = self.NovaPoshtaSerializer(obj, context=self.context)
            return serializer.data

        def get_ukrPoshta(self, obj) -> ReturnDict[Any, Any]:
            serializer = self.UkrPostaSerializer(obj, context=self.context)
            return serializer.data

        def get_address(self, obj) -> ReturnDict[Any, Any]:
            serializer = self.AddressSerializer(obj, context=self.context)
            return serializer.data

    class OutputAuthUserSerializer(serializers.ModelSerializer):
        novaPoshta = inline_serializer(
            name="novaPoshta",
            required=False,
            fields={
                "nova_poshta_town": serializers.CharField(required=False),
                "nova_poshta_post_office": serializers.CharField(required=False),
            },
        )
        ukrPoshta = inline_serializer(
            name="ukrPoshta",
            required=False,
            fields={
                "ukr_poshta_town": serializers.CharField(required=False),
                "ukr_poshta_post_office": serializers.CharField(required=False),
            },
        )
        address = inline_serializer(
            name="address",
            required=False,
            fields={
                "address_town": serializers.CharField(required=False),
                "address_street": serializers.CharField(required=False),
                "address_building": serializers.CharField(required=False),
                "address_flat": serializers.CharField(required=False),
            },
        )
        gender = serializers.CharField(source="get_gender_display")
        role = serializers.CharField(source="get_role_display")

        class Meta:
            model = User
            fields = [
                "email",
                "first_name",
                "last_name",
                "mobile",
                "dob",
                "address",
                "novaPoshta",
                "ukrPoshta",
                "gender",
                "role",
                "notice",
                "get_age",
            ]

    @extend_schema(
        responses={
            200: OutputAuthUserSerializer,
        },
    )
    def get(self, request):
        user: User = request.user
        return Response(self.UserSerializer(user).data)

    @extend_schema(
        request=OutputAuthUserSerializer,
        responses={
            200: OutputAuthUserSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        user: User = request.user
        serializer = self.UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        nova_poshta_data = serializer.initial_data.get("novaPoshta")
        if nova_poshta_data:
            nova_poshta_serializer = self.UserSerializer.NovaPoshtaSerializer(
                user, data=nova_poshta_data, partial=True
            )
            if nova_poshta_serializer.is_valid():
                nova_poshta_serializer.save()

        ukr_poshta_data = serializer.initial_data.get("ukrPoshta")
        if ukr_poshta_data:
            ukr_poshta_serializer = self.UserSerializer.UkrPostaSerializer(
                user, data=ukr_poshta_data, partial=True
            )
            if ukr_poshta_serializer.is_valid():
                ukr_poshta_serializer.save()

        address_data = serializer.initial_data.get("address")
        if address_data:
            address_serializer = self.UserSerializer.AddressSerializer(
                user, data=address_data, partial=True
            )
            if address_serializer.is_valid():
                address_serializer.save()

        return Response(serializer.data)


class GetOrdersHistory(APIView):
    """
    Return orders history for current user
    """
    permission_classes = [IsAuthenticated, AuthUserPermission]

    class OutputSwaggerSerializer(serializers.ModelSerializer):
        products = inline_serializer(
            name="product",
            required=False,
            fields={
                "product": serializers.UUIDField(required=False),
                "name": serializers.CharField(required=False),
                "img": serializers.CharField(required=False),
                "quantity": serializers.IntegerField(required=False),
                "price": serializers.DecimalField(required=False, max_digits=10, decimal_places=2),
            },
        )

        class Meta:
            model = Order
            fields = (
                "id",
                "status",
                "order_date",
                "products",
            )

    class OutputOrdersHistory(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = (
                "id",
                "status",
                "order_date",
                "products",
            )

        class OredrItemSerializer(serializers.ModelSerializer):
            class Meta:
                model = OrderItem
                fields = ("product", "name", "img", "quantity", "price")

        products = serializers.SerializerMethodField()

        def get_products(self, obj):
            serializer = self.OredrItemSerializer(
                obj.orderitem_set.all(), many=True, context={"request": self.context.get("request")}
            )
            return serializer.data

    @extend_schema(
        tags=["Auth_user"],
        responses={200: OutputSwaggerSerializer},
    )
    def get(self, request):
        user: User = request.user
        orders = Order.objects.filter(customer=user)
        serializer = self.OutputOrdersHistory(orders, many=True, context={"request": request})
        return Response(serializer.data)
