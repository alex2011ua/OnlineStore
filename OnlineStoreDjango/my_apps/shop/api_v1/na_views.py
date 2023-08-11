from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from my_apps.shop.models import Product
from my_apps.shop.models import Settings

from .serializers import ProductSerializer


class ListPopularGifts(APIView):
    """
    List most popular products with rate > RED_LINE.
    """

    rate_limit, _ = Settings.objects.get_or_create(
        name="rate_limit",
        defaults={"description": "show gifts with rate more then value", "value": 6},
    )
    red_line = rate_limit.value

    def get(self, request, format=None):
        products = Product.objects.filter(global_rating__gt=self.red_line).order_by(
            "-sold"
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
