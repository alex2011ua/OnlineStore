from uuid import UUID

from django.contrib.auth import get_user
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
    OpenApiResponse,
)
from my_apps.accounts.models import User
from my_apps.shop.api_v1.auth_user.serializers_auth_user import (
    ProductIdSerializer,
    ProductSerializer,
)
from my_apps.shop.api_v1.permissions import AuthUserPermission
from my_apps.shop.api_v1.serializers import BasketSerializer
from my_apps.shop.models import Order, OrderItem, Product
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(tags=["Auth_user"])
class TestAuthUser(APIView):
    """test permissions"""

    permission_classes = [IsAuthenticated, AuthUserPermission]

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})


@extend_schema(
    tags=["Auth_user"],
    request=inline_serializer(
        name="InlineFormSerializer",
        fields={
            "product_id": serializers.UUIDField(),
            "amount": serializers.IntegerField(),
        },
    ),
)
@extend_schema_view(
    delete=extend_schema(
        summary="delete product from basket",
        parameters=[
            OpenApiParameter(
                name="product_id",
                location=OpenApiParameter.QUERY,
                description="product id",
                required=True,
                type=UUID,
            ),
        ],
    ),
)
class Basket(APIView):
    permission_classes = [IsAuthenticated, AuthUserPermission]

    def post(self, request):
        serializer = BasketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id: str = serializer.validated_data.get("product_id")
        amount: int = serializer.validated_data.get("amount")

        product = Product.get_by_id(product_id)
        user: User = request.user
        order = Order.get_current_order_id(user)
        order.add_product_to_order(product, amount)
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user: User = request.user
        order = Order.get_current_order_id(user)
        return Response({"order_id": order.id, "products": order.get_products_order()})

    def delete(self, request):
        user: User = request.user
        product_id: str = request.query_params.get("product_id")
        product = Product.get_by_id(product_id)
        order = Order.get_current_order_id(user)
        order.delete_product_order(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Auth_user"],
    request=ProductIdSerializer,
)
@extend_schema_view(
    get=extend_schema(
        summary="get all wishlist for user",
        responses={
            status.HTTP_200_OK: ProductIdSerializer,
        },
    ),
    post=extend_schema(
        summary="add product in wishlist",
        responses={
            status.HTTP_200_OK: ProductIdSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=False,
                description="Authentication credentials were not provided.",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=False, description="Product not found."
            ),
        },
    ),
    delete=extend_schema(
        summary="delete product from wishlist",
        request=ProductIdSerializer,
        responses={
            status.HTTP_200_OK: ProductIdSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.QUERY,
                description="product id",
                required=True,
                type=UUID,
            ),
        ],
    ),
)
class Wishlist(APIView):
    permission_classes = [IsAuthenticated, AuthUserPermission]

    def get(self, request):
        user = get_user(request)
        products = ProductSerializer(user.wishlist.all(), many=True)
        for product in products.data:
            product["wishlist"] = True
        return Response(products.data)

    def post(self, request):
        user = get_user(request)
        serializer = ProductIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.get_by_id(serializer.validated_data["id"])
        user.wishlist.add(product)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = get_user(request)
        serializer = ProductIdSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        product = Product.get_by_id(serializer.validated_data["id"])
        user.wishlist.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
