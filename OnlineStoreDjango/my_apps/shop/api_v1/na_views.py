from rest_framework.response import Response
from rest_framework.views import APIView
from .paginators import SmallResultsSetPagination
from random import randint
from my_apps.shop.models import Product
from my_apps.shop.models import Settings

from .serializers import ProductSerializer


class ListPopularGifts(APIView, SmallResultsSetPagination):
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
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class ListSearchGifts(APIView, SmallResultsSetPagination):
    """Search by name and slug."""

    def get(self, request, format=None):
        search_string = request.query_params["search"]
        products1 = Product.objects.filter(slug__icontains=search_string)
        products2 = Product.objects.filter(name__icontains=search_string)
        products = products1 | products2
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class ListNewGifts(APIView, SmallResultsSetPagination):
    """Return products ordered by date of creation."""

    def get(self, request, format=None):
        products = Product.objects.all().order_by("-created_at")[:30]
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class RandomGift(APIView):
    """Return product according to input price"""

    def get(self, request):
        from_price = request.query_params.get("from", 0)
        to_price = request.query_params.get("to", 1000000)

        # get quantity of products according to price filter and choose random index
        random_index = randint(
            0,
            Product.objects.filter(price__gte=float(from_price), price__lte=to_price).count() - 1,
        )
        product = Product.objects.filter(
            price__gte=float(from_price), price__lte=to_price
        )[random_index]
        serializer = ProductSerializer(product)
        return Response(serializer.data)
