from random import randint, sample
from uuid import UUID

from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema, extend_schema_view)
from my_apps.shop.models import (Banner, Category, Order, OrderItem, Product,
                                 Settings)
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .paginators import SmallResultsSetPagination, StandardResultsSetPagination
from .serializers import (BannerSerializer, CategorySerializer,
                          ProductSerializer)


def version_uuid(uuid):
    try:
        return UUID(uuid).version
    except ValueError:
        return None


@extend_schema(tags=["Guest_user"])
class TestGuestUser(APIView):
    """Return product according to input price"""

    def get(self, request):
        return Response({"detail": "Test_OK", "code": "Test permission OK"})


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="most popular products with rate > 3",
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="page",
                location=OpenApiParameter.QUERY,
                description="page of pagination",
                type=int,
            ),
        ],
    ),
)
class ListPopularGifts(APIView, SmallResultsSetPagination):
    """
    List most popular products with rate > 3.
    """

    rate_limit, _ = Settings.objects.get_or_create(
        name="rate_limit",
        defaults={"description": "show gifts with rate more then value", "value": 6},
    )
    red_line = 3  # rate_limit.value

    def get(self, request, format=None):
        products = Product.objects.filter(global_rating__gt=3).order_by("-sold")
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, context={"request": request}, many=True)
        return self.get_paginated_response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="Search by name and slug",
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="page",
                location=OpenApiParameter.QUERY,
                description="page of pagination",
                type=int,
            ),
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                description="search string",
                type=str,
            ),
        ],
    ),
)
class ListSearchGifts(APIView, SmallResultsSetPagination):
    """Search products by name and slug."""

    def get(self, request, format=None):
        search_string = request.query_params.get("search", None)
        if search_string is None:
            data = {"detail": "required search param", "code": "required_search"}
            return Response(status=status.HTTP_417_EXPECTATION_FAILED, data=data)

        products1 = Product.objects.filter(slug__icontains=search_string)
        products2 = Product.objects.filter(name__icontains=search_string)
        products = products1 | products2
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, context={"request": request}, many=True)
        return self.get_paginated_response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="Return products ordered by date of creation.",
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="page",
                location=OpenApiParameter.QUERY,
                description="page of pagination",
                type=int,
            )
        ],
    ),
)
class ListNewGifts(APIView, SmallResultsSetPagination):
    """Return products ordered by date of creation with pagination and limit=30"""

    def get(self, request, format=None):
        products = Product.objects.all().order_by("-created_at")[:30]
        results = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(results, context={"request": request}, many=True)
        return self.get_paginated_response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="get random product",
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_404_NOT_FOUND: {
                "coed": status.HTTP_404_NOT_FOUND,
                "details": "category is empty",
            },
        },
        parameters=[
            OpenApiParameter(
                name="from",
                location=OpenApiParameter.QUERY,
                description="start price of product, default=0",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="to",
                location=OpenApiParameter.QUERY,
                description="end price of product, default=1000000",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="category",
                location=OpenApiParameter.QUERY,
                description="search in category",
                required=False,
                type=str,
            ),
        ],
    ),
)
class RandomGift(APIView):
    """Return product according to input price and category"""

    def get(self, request):
        from_price = request.query_params.get("from", 0)
        to_price = request.query_params.get("to", 1000000)
        category_id = request.query_params.get("category", None)
        if category_id and version_uuid(category_id) != 4:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data=["Wrong ID category"]
            )

        products = Product.get_products_in_category(
            category_id
        )  # add product in this category and subcategories
        products_filtered_by_price = products.filter(
            price__gte=float(from_price), price__lte=to_price
        )
        if products_filtered_by_price.count() == 0:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data=["no products in this category"]
            )

        random_index = randint(0, products_filtered_by_price.count() - 1)
        product = products_filtered_by_price[random_index]
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="get random products",
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="from",
                location=OpenApiParameter.QUERY,
                description="start price of product, default=0",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="to",
                location=OpenApiParameter.QUERY,
                description="end price of product, default=1000000",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="quantity",
                location=OpenApiParameter.QUERY,
                description="quantity of products to return, default=5",
                required=False,
                type=int,
            ),
        ],
    ),
)
class ListRandomGifts(APIView):
    """Return list of products according to input price"""

    def get(self, request):
        from_price = request.query_params.get("from", 0)
        to_price = request.query_params.get("to", 1000000)
        count = int(request.query_params.get("quantity", 5))

        products = list(
            Product.objects.filter(price__gte=float(from_price), price__lte=to_price)
        )
        if len(products) < count:
            count = len(products)
        serializer = ProductSerializer(
            sample(products, count), context={"request": request}, many=True
        )
        return Response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="get all banners",
        responses={
            status.HTTP_200_OK: BannerSerializer,
        },
    ),
)
class ListBanners(ListAPIView):
    """
    Return list of banners.
    """

    pagination_class = None
    model = Banner
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="GPT test",
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                description="search string",
                type=str,
            ),
        ],
    ),
)
class Gpt(APIView):
    """Search products by name and slug."""

    def get(self, request, format=None):
        search_string = request.query_params.get("search", None)
        if search_string is None:
            data = {"detail": "required search param", "code": "required_search"}
            return Response(status=status.HTTP_417_EXPECTATION_FAILED, data=data)
        from my_apps.shop.llama import LlamaSearch

        search = LlamaSearch()
        s = search.search_answer(search_string)
        return Response(s)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    list=extend_schema(
        summary="all categories with sub categories",
        responses={
            status.HTTP_200_OK: CategorySerializer,
        },
    ),
)
class GetAllCategories(viewsets.ViewSet):
    """
    Endpoint to get all categories with sub categories
    """

    def list(self, request):
        queryset = Category.get_main_categories()
        serializer = CategorySerializer(
            queryset, context={"request": request}, many=True
        )
        return Response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    list=extend_schema(
        summary="products in category filtered and ordered",
        responses={
            status.HTTP_200_OK: ProductSerializer,
            422: OpenApiResponse(description="wrong query param: "),
            404: OpenApiResponse(description="category not found "),
        },
        parameters=[
            OpenApiParameter(
                name="page",
                location=OpenApiParameter.QUERY,
                description="page",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="sort",
                location=OpenApiParameter.QUERY,
                description="cheap | expensive | new | popular | rate",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="price_from",
                location=OpenApiParameter.QUERY,
                description="price_from",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="price_to",
                location=OpenApiParameter.QUERY,
                description="price_to",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="main",
                location=OpenApiParameter.QUERY,
                description="main(available |& pending  |& available)",
                required=False,
                type=str,
            ),
        ],
    ),
)
class GetProductsByCategory(viewsets.ViewSet, StandardResultsSetPagination):
    def list(self, request, category_id):
        match request.query_params.get("sort"):
            case "cheap":
                order_by = "price"
            case "expensive":
                order_by = "-price"
            case "new":
                order_by = "-created_at"
            case "popular":
                order_by = "-sold"
            case "rate":
                order_by = "-global_rating"
            case _:
                order_by = "name"
        category = Category.get_by_id(category_id)
        params_filtering = {"category": category}
        # sort by price
        if request.query_params.get("price_from"):
            params_filtering["price__gte"] = request.query_params.get("price_from")
        if request.query_params.get("price_to"):
            params_filtering["price__lte"] = request.query_params.get("price_to")
        # sort by rating
        if request.query_params.get("rate"):
            params_filtering["global_rating__gte"] = request.query_params.get("rate")
        #  add list of main filters
        for product_filter in request.query_params.getlist("main"):
            match product_filter:
                case "available":
                    # add only available products whith quantity > 0
                    params_filtering["quantity__gt"] = 0
                case "pending":
                    # add only products whith quantity = 0
                    params_filtering["quantity"] = 0
                case "sale":
                    # only product with discount
                    params_filtering["discount__gt"] = 0
                case _:
                    return Response(
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data=[f"wrong query param: {product_filter}"],
                    )

        queryset = Product.objects.filter(**params_filtering).order_by(order_by)

        results = self.paginate_queryset(queryset, request, view=self)
        serializer = ProductSerializer(results, context={"request": request}, many=True)
        return self.get_paginated_response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    retrieve=extend_schema(
        summary="return product info",
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
    ),
)
class GetProduct(viewsets.ViewSet):
    def retrieve(self, request, product_id):
        product = Product.get_by_id(product_id)
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)
