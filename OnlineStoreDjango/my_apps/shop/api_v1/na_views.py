from rest_framework.views import APIView
from .paginators import SmallResultsSetPagination
from django.db.models import Q

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
    def get(self, request, format=None):
        search_string = request.query_params["search"]
        products = Product.objects.filter(
            Q(slug__icontains=search_string) and Q(name__icontains=search_string)
        )
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class ListNewGifts(APIView, SmallResultsSetPagination):
    def get(self, request, format=None):

        products = Product.objects.all().order_by("-created_at")[:30]
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
