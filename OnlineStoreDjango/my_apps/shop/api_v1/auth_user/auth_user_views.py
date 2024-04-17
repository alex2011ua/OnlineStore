from typing import Any
from uuid import UUID

from django.contrib.auth import get_user
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers, status, viewsets
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView

from my_apps.accounts.models import User
from my_apps.shop.api_v1.auth_user.serializers_auth_user import (
    ProductIdSerializer,
    ProductSerializer,
)
from my_apps.shop.api_v1.guest_user.guest_user_views import ListSearchGifts
from my_apps.shop.api_v1.permissions import AuthUserPermission
from my_apps.shop.api_v1.serializers import (
    BasketItemSerializer,
    BasketSerializer,
    CreateReviewSerializer,
    ReviewSerializer,
)
from my_apps.shop.models import BasketItem, Product, Review


@extend_schema(tags=["Auth_user"])
class TestAuthUser(APIView):
    """test permissions"""

    permission_classes = [IsAuthenticated, AuthUserPermission]

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})


@extend_schema_view(
    tags=["Auth_user"],
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
    """Endpoint for get post and delete products in basket current user."""

    permission_classes = [IsAuthenticated, AuthUserPermission]

    class InputBasketSerializer(serializers.Serializer):
        product_id = serializers.UUIDField()
        amount = serializers.IntegerField()
        isSecretPresent = serializers.BooleanField(default=False, required=False)

    @extend_schema(
        tags=["Auth_user"],
        description="add list products to basket",
        request=InputBasketSerializer(many=True),
    )
    def post(self, request):
        serializer = self.InputBasketSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for data in serializer.validated_data:
            product_id: str = data.get("product_id")
            amount: int = data.get("amount")
            is_secret_present: bool = data.get("isSecretPresent", False)

            product: Product = Product.get_by_id(product_id)
            user: User = request.user

            BasketItem.objects.update_or_create(
                product=product,
                defaults={
                    "quantity": amount,
                    "registered_user": user,
                    "is_secret_present": is_secret_present,
                },
            )
        return Response(status=status.HTTP_200_OK)

    class BasketOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = (
                "id",
                "img",
                "name",
                "category",
                "price",
                "global_rating",
                "discount",
                "quantity",
                "count",
                "isSecretPresent",
            )

        id = serializers.UUIDField()
        name = serializers.CharField()
        category = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)
        global_rating = serializers.IntegerField()
        discount = serializers.DecimalField(max_digits=5, decimal_places=2)
        quantity = serializers.IntegerField()
        isSecretPresent = serializers.BooleanField()
        count = serializers.IntegerField()

    @extend_schema(
        tags=["Auth_user"],
        description="get list products in basket",
        request=BasketItemSerializer(many=True),
    )
    def get(self, request):
        """
                [
        {
          id: string;
          img: string;
          name: string;
          / Category of product (type of product) */
          category: string;
          price: number;
          global_rating: number;
          discount: number;
          //  Count of a product in a store
          quantity: number;
        // скільки продукту додав у кошик користувач
          count: number;
        // чи це секретний подарунок
          isSecretPresent: boolean;
        }

        ]
        """
        user: User = request.user
        basket = user.basket.all()
        data = []
        for item in basket:
            product = Product.get_by_id(item.product_id)
            data.append(
                {
                    "id": product.id,
                    "img": product.img,
                    "name": product.name,
                    "category": product.get_category_name(),
                    "price": product.price,
                    "global_rating": product.global_rating,
                    "discount": product.discount,
                    "quantity": product.quantity,
                    "isSecretPresent": item.is_secret_present,
                    "count": item.quantity,
                }
            )
        serializer = self.BasketOutputSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        tags=["Auth_user"],
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
    )
    def delete(self, request):
        user: User = request.user
        product_id: str = request.query_params.get("product_id")
        product = Product.get_by_id(product_id)
        try:
            user.basket.get(registered_user=user, product=product).delete()
        except BasketItem.DoesNotExist:
            raise NotFound
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Auth_user"],
    summary="removing all products from the basket for an authorized user",
)
class BasketClear(APIView):
    permission_classes = [IsAuthenticated, AuthUserPermission]

    def delete(self, request):
        user: User = request.user
        user.basket.filter(registered_user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Auth_user"],
    request=ProductIdSerializer,
)
@extend_schema_view(
    get=extend_schema(
        summary="get all wishlist for user",
        description="get all wishlist for user",
        responses={
            status.HTTP_200_OK: ProductIdSerializer,
        },
    ),
    post=extend_schema(
        summary="add product in wishlist",
        description="add product in wishlist",
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
        summary="delete products from wishlist",
        description="delete one or more products from wishlist",
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
                many=True,
            ),
        ],
    ),
)
class Wishlist(APIView):
    """Endpoint for get post and delete products in wishlist current user."""

    permission_classes = [IsAuthenticated, AuthUserPermission]

    def get(self, request):
        user: User = request.user
        products = ProductSerializer(user.wishlist.all(), many=True, context={"request": request})  # type: ignore
        for product in products.data:
            product["wishlist"] = True
        return Response(products.data)

    def post(self, request):
        user: User = request.user
        serializer = ProductIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.get_by_id(serializer.validated_data["id"])
        user.wishlist.add(product)  # type: ignore
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request) -> Response:
        user: User = request.user
        id_values = self.request.query_params.getlist("id")
        for id_value in id_values:
            serializer = ProductIdSerializer(data={"id": id_value})
            serializer.is_valid(raise_exception=True)
            product = Product.get_by_id(serializer.validated_data["id"])
            user.wishlist.remove(product)  # type: ignore
        return Response(status=status.HTTP_204_NO_CONTENT)


class DelListProducts(APIView):
    class InputSerializer(serializers.Serializer):
        product_id = serializers.ListSerializer(child=serializers.UUIDField())

    @extend_schema(
        tags=["Auth_user"],
        summary="delete products from wishlist",
        request=InputSerializer,
        responses={204: []},
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        list_id = serializer.validated_data["product_id"]
        for id_value in list_id:
            serializer = ProductIdSerializer(data={"id": id_value})
            serializer.is_valid(raise_exception=True)
            product = Product.get_by_id(serializer.validated_data["id"])
            user.wishlist.remove(product)  # type: ignore
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Auth_user"],
    request=ReviewSerializer,
)
class AuthComments(APIView):
    permission_classes = [IsAuthenticated, AuthUserPermission]

    def post(self, request, pk):
        product = Product.get_by_id(pk)
        data = request.data.copy()
        serializer = CreateReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        comment = Review.objects.create(
            author=request.user, product=product, **serializer.validated_data
        )
        return Response(comment.id)

