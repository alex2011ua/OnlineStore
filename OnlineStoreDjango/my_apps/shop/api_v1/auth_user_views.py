from drf_spectacular.utils import extend_schema, inline_serializer
from my_apps.accounts.models import User
from my_apps.shop.api_v1.permissions import AuthUserPermission
from my_apps.shop.api_v1.serializers import OrderSerializer, ProductSerializer
from my_apps.shop.models import Order, OrderItem, Product
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

"""
1. 
"""


@extend_schema(tags=["Auth_user"])
class TestAuthUser(APIView):
    """Return product according to input price"""

    permission_classes = [IsAuthenticated, AuthUserPermission]

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})


@extend_schema(
    tags=["Auth_user"],
    request=inline_serializer(
        name="InlineFormSerializer",
        fields={
            "product": serializers.UUIDField(),
            "amount": serializers.IntegerField(),
        },
    ),
)
class AddProductOrder(APIView):
    permission_classes = [IsAuthenticated, AuthUserPermission]

    def post(self, request):
        product_id: str = request.data.get("product")
        product = Product.get_by_id(product_id)
        if not product:
            raise NotFound(detail="Error 404, product not found", code=404)
        amount: int = int(request.data.get("amount"))

        user: User = request.user
        order = Order.get_current_order_id(user)
        products_in_order = order.products.all()
        if product in products_in_order:
            oi = OrderItem.objects.get(product=product)
            oi.quantity = amount
            oi.save()
        else:
            order.products.add(product, through_defaults={"quantity": amount})
        oi = OrderItem.objects.filter(order=order)
        product_list_in_order: list = []
        for prod in oi:
            product_list_in_order.append(
                {"prodID": prod.product.id, "quantity": prod.quantity}
            )
        return Response({"order_id": order.id, "products": product_list_in_order})


"""
{
  "order_id": "dfd81a6e-6f98-40db-a1a9-4c3e398947ad",
  "products": [
    {
      "prodID": "97e0cbde-961f-405c-8feb-70bd2c7e347f",
      "quantity": 3
    },
    {
      "prodID": "a996be29-687d-4d3f-ae92-fd0af736f804",
      "quantity": 5
    }
  ]
}
"""


class GetOrderInfo(APIView):
    def get(self, request):
        return Response({})
