from django.contrib.postgres.search import SearchVector
import logging
from random import sample
from uuid import UUID

from django.core.mail import send_mail
from django.db.models import QuerySet
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from my_apps.shop.models import Banner, Category, Order, OrderItem, Product, Settings

from .paginators import StandardResultsSetPagination
from .serializers import (
    BannerSerializer,
    CategorySerializer,
    ProductCardSerializer,
    ProductCatalogSerializer,
    ReviewSerializer,
)

logger = logging.getLogger("main")


def version_uuid(uuid: str) -> bool:
    """Verification of incoming text as UUID."""
    try:
        return UUID(uuid).version == 4
    except ValueError:
        return False



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
    if len(request.query_params.getlist("rate")) > 0:
        rate_list: list = []
        for rate_ in request.query_params.getlist("rate"):
            rate_list.append(rate_)
        params_filtering["global_rating__in"] = rate_list

    #  add list of main filters
    for product_filter in request.query_params.getlist("main"):
        match product_filter:
            case "available":
                # add only available products with quantity > 0
                params_filtering["quantity__gt"] = 0
            case "pending":
                # add only products with quantity = 0
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
@extend_schema_view(
    get=extend_schema(
        summary="Search by name and slug",
        responses={
            status.HTTP_200_OK: ProductCatalogSerializer,
            417: OpenApiResponse(description="required search param"),
            422: OpenApiResponse(description="wrong query param: "),
        },
        parameters=[
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                description="search string",
                type=str,
                required=False,
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
            OpenApiParameter(
                name="rate",
                location=OpenApiParameter.QUERY,
                description="rate",
                required=False,
                type=int,
            ),
        ],
    ),
)
class ListSearchGifts(APIView, StandardResultsSetPagination):  # type: ignore
    """Search products by name, slug and category name."""

    def get(self, request):
        search_string: None | str = request.query_params.get("search", None)

        if search_string:
            products1: QuerySet = Product.objects.select_related("category").filter(
                slug__icontains=search_string
            )
            products2 = Product.objects.select_related("category").filter(
                name__icontains=search_string
            )
            products3 = Product.objects.select_related("category").filter(
                category__name__icontains=search_string
            )
            products = products1 | products2 | products3  # get products according to search string
            logger.info(
                "ListSearchGifts - search_string:"
                + search_string
                + "; count: "
                + str(len(products))
            )
        else:
            products = Product.objects.select_related("category").all()

        filtered_products = products_filter_sort(
            request, products
        )  # get filtered and sorted products

        results = self.paginate_queryset(filtered_products, request, view=self)
        serializer = ProductCatalogSerializer(results, context={"request": request}, many=True)
        return self.get_paginated_response(serializer.data)

    # def get_queryset(self):
    #     logging.warning("sdfsvefsdvdfvdf")
    #     queryset = Product.objects.all()
    #     search_string: None | str = self.request.query_params.get("search", None)
    #     if search_string:
    #         search_vector = SearchVector("slug", "name", "category__name")
    #         queryset = queryset.annotate(search=search_vector).filter(search=search_string)
    #     filtered_products = products_filter_sort(
    #             self.request, queryset
    #         )  # get filtered and sorted products
    #     logging.warning(filtered_products)
    #     return filtered_products


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    get=extend_schema(
        summary="get random products",
        responses={
            status.HTTP_200_OK: ProductCatalogSerializer,
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
    """Return list of products according to input price.
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
            products_queryset: QuerySet = Product.objects.select_related("category").all()
        products = list(products_queryset.filter(price__gte=float(from_price), price__lte=to_price))
        if len(products) < count:  # if count products less as existing, correct count
            count = len(products)
        # get random products from products list
        serializer = ProductCatalogSerializer(
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
            status.HTTP_200_OK: ProductCatalogSerializer,
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

    def get(self, request):
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
    """Endpoint to get all categories with sub categories."""

    def list(self, request):
        queryset = Category.get_main_categories()
        serializer = CategorySerializer(queryset, context={"request": request}, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Guest_user"])
@extend_schema_view(
    list=extend_schema(
        summary="products in category filtered and ordered",
        responses={
            status.HTTP_200_OK: ProductCatalogSerializer,
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
            OpenApiParameter(
                name="rate",
                location=OpenApiParameter.QUERY,
                description="rate",
                required=False,
                type=int,
            ),
        ],
    ),
)
class GetProductsByCategory(viewsets.ViewSet, StandardResultsSetPagination):  # type: ignore
    """Get filtered and sorted product in given category."""

    def list(self, request, category_id):
        category = Category.get_by_id(category_id)
        products = Product.objects.prefetch_related("category").filter(
            category=category
        )  # get all products in category
        filtered_products = products_filter_sort(
            request, products
        )  # get filtered and sorted product
        results = self.paginate_queryset(filtered_products, request, view=self)
        serializer = ProductCatalogSerializer(results, context={"request": request}, many=True)
        return self.get_paginated_response(serializer.data)


@extend_schema(tags=["Guest_user"])
class GetProduct(viewsets.ReadOnlyModelViewSet):
    """Get product by ID."""

    queryset = Product.objects.all()
    serializer_class = ProductCardSerializer
    pagination_class = None

    @extend_schema(
        tags=["Guest_user"],
        responses={200: ProductCatalogSerializer},
        parameters=[
            OpenApiParameter(
                name="product_id",
                location=OpenApiParameter.QUERY,
                description="product_id",
                required=False,
                type=str,
            )
        ],
    )
    def list(self, request):
        list_id = request.query_params.getlist("product_id")
        queryset = Product.objects.filter(pk__in=list_id)
        serializer = ProductCatalogSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


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
    """Get category ID by category slug."""
    if request.method == "GET":
        cat = Category.get_category(url_category)
        return Response(cat.id)


@extend_schema(
    tags=["Guest_user"],
    responses={
        404: OpenApiResponse(description="product not found "),
        200: ReviewSerializer,
    },
    summary="get all reviews in product",
)
class Comments(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List comments in given product."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs["prod_pk"]
        product = Product.get_by_id(product_id)
        return product.reviews.all()


@extend_schema(
    tags=["Guest_user"],
    summary="store info",
)
@api_view(["GET"])
def store_info(request):
    """
    get an array of objects title and text:
        "agreement",
        "payment_delivery",
        "return_conditions",
        "privacy_policy".
    """

    agreement = Settings.objects.get(name_en="agreement")
    payment_delivery = Settings.objects.get(name_en="payment_delivery")
    return_conditions = Settings.objects.get(name_en="return_conditions")
    privacy_policy = Settings.objects.get(name_en="privacy_policy")

    return Response(
        [
            agreement.to_dict(),
            payment_delivery.to_dict(),
            return_conditions.to_dict(),
            privacy_policy.to_dict(),
        ]
    )
