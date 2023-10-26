from random import randint, sample
from uuid import UUID

from django.db.models import QuerySet
from django.utils.translation import get_language
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.exceptions import NotFound

from my_apps.shop.models import Banner, Category, Order, OrderItem, Product, Settings
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .paginators import SmallResultsSetPagination, StandardResultsSetPagination
from .serializers import (
    BannerSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
)


def version_uuid(uuid):
    try:
        return UUID(uuid).version
    except ValueError:
        return None


def products_filter_sort(request, queryset):
    """
     Filter and sort queryset.

     sorts: {
       cheap
       expensive
       new
       popular
       rate
     },
    filters: {
       sale
       pending
       available
     },
     price_from,
     price_to,
     rate,
    """
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

    params_filtering = {}
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
    filtered_queryset = queryset.filter(**params_filtering).order_by(order_by)
    return filtered_queryset


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
class ListPopularGifts(APIView, StandardResultsSetPagination):
    """
    List most popular products with rate > 3.
    """
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
            417: OpenApiResponse(description="required search param"),
            422: OpenApiResponse(description="wrong query param: "),
        },
        parameters=[
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                description="search string",
                type=str,
            ),
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
                description="main(available |& pending  |& sale)",
                required=False,
                type=str,
            ),
        ],
    ),
)
class ListSearchGifts(APIView, StandardResultsSetPagination):
    """Search products by name and slug."""

    def get(self, request, format=None):
        search_string = request.query_params.get("search", None)
        if search_string is None:
            data = {"detail": "required search param"}
            return Response(status=status.HTTP_417_EXPECTATION_FAILED, data=data)

        products1 = Product.objects.filter(slug__icontains=search_string)
        products2 = Product.objects.filter(name__icontains=search_string)
        products = products1 | products2  # get products according to search string
        filtered_products = products_filter_sort(
            request, products
        )  # get filtered and sorded products
        results = self.paginate_queryset(filtered_products, request, view=self)
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
        summary="get random products",
        responses={
            status.HTTP_200_OK: ProductSerializer,
            404: OpenApiResponse(description="id not UUID or not found"),
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
                description="end price of product, default=2000",
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
            OpenApiParameter(
                name="categoryId",
                location=OpenApiParameter.QUERY,
                description="search in category",
                required=False,
                type=str,
            ),
        ],
    ),
)
class ListRandomGifts(APIView):
    """Return list of products according to input price
    price_from: number (default: 0)
    price_to: number (default: 2000)
    quantity: number (default: 5)
    categoryId: string
    """

    def get(self, request):
        from_price = request.query_params.get("from", 0)
        to_price = request.query_params.get("to", 2000)
        count = int(request.query_params.get("quantity", 5))
        category_id = request.query_params.get("categoryId", None)

        if category_id:
            products_queryset: QuerySet = Product.get_products_in_category(category_id)
        else:
            products_queryset: QuerySet = Product.objects.all()
        products = list(
            products_queryset.filter(price__gte=float(from_price), price__lte=to_price)
        )
        if len(products) < count:  # if count products less as existing, correct count
            count = len(products)
        # get random products from products list
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
class ListBanners(generics.ListAPIView):
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
                description="main(available |& pending  |& sale)",
                required=False,
                type=str,
            ),
        ],
    ),
)
class GetProductsByCategory(viewsets.ViewSet, StandardResultsSetPagination):
    def list(self, request, category_id):
        category = Category.get_by_id(category_id)
        products = Product.objects.filter(
            category=category
        )  # get all products in category
        filtered_products = products_filter_sort(
            request, products
        )  # get filtered and sorted product
        results = self.paginate_queryset(filtered_products, request, view=self)
        serializer = ProductSerializer(results, context={"request": request}, many=True)
        return self.get_paginated_response(serializer.data)


@extend_schema(tags=["Guest_user"])
class GetProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(
    tags=["Guest_user"],
    responses={
        200: OpenApiResponse(description="return ID category "),
        404: OpenApiResponse(description="category not found "),
    },
    summary="get category by slug",
)
@api_view()
def get_category_by_slug(request, url_category):
    if request.method == "GET":
        cat = Category.get_category(url_category)
        return Response(cat.id)

@extend_schema(
    tags=["Guest_user"],
    responses={
        404: OpenApiResponse(description="product not found "),
    },
    summary="get all reviews in product",
)
class Comments(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):

        product_id = self.kwargs["prod_pk"]
        product = Product.get_by_id(product_id)
        return product.reviews.all()
