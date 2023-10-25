import pytest
from django.shortcuts import redirect
from my_apps.accounts.models import User
from my_apps.shop.models import Category, Product
from rest_framework.test import APIRequestFactory, force_authenticate

from .auth_user_views import Basket
from my_apps.shop.api_v1.guest_user_views import Comments
from my_apps.shop.api_v1.auth_user.auth_user_views import AuthComments


@pytest.fixture(autouse=True)
def initalized_task_db(tmpdir):
    category1 = Category.objects.create(name="cat1", slug="slugcat1")
    category2 = Category.objects.create(name="cat2", slug="slugcat2")
    product1 = Product.objects.create(
        name="prod1", slug="prod1", category=category1, price=1
    )
    product2 = Product.objects.create(
        name="prod2", slug="prod2", category=category2, price=3
    )
    product3 = Product.objects.create(
        name="prod3", slug="prod3", category=category1, price=3
    )
    user_auth = User.objects.create(email="auth_user@gmail.com", role="U")


@pytest.mark.django_db
def test_basket_endpoints():
    factory = APIRequestFactory()
    user = User.objects.get(email="auth_user@gmail.com")
    view = Basket.as_view()

    request = factory.get(redirect("auth_user_basket"))
    force_authenticate(request, user=user)
    response = view(request)
    assert response.data == []

    p = Product.objects.all()[0]
    request = factory.post(
        redirect("auth_user_basket"), {"product_id": p.id, "amount": 2}
    )
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200

    request = factory.get(redirect("auth_user_basket"))
    force_authenticate(request, user=user)
    response = view(request)
    assert response.data != []
    assert len(response.data) == 1


@pytest.mark.django_db
def test_product_review():
    """test getting and creating review in product"""
    factory = APIRequestFactory()
    product = Product.objects.filter()[0]
    user = User.objects.get(email="auth_user@gmail.com")
    request_get_reviews = factory.get(
        redirect("get_product_comments", prod_pk=product.id)
    )
    view_get_comment = Comments.as_view({"get": "list"})
    request_add_review = factory.post(
        redirect("auth_comments", pk=product.id), {"title": "string", "body": "string"}
    )
    # count comments should be 0
    response = view_get_comment(request_get_reviews, prod_pk=product.id)
    assert response.data["count"] == 0
    # add new comment
    force_authenticate(request_add_review, user=user)
    view = AuthComments.as_view()
    response = view(request_add_review, pk=product.id)
    assert response.status_code == 200
    # count comments should be 1
    response = view_get_comment(request_get_reviews, prod_pk=product.id)
    assert response.data["count"] == 1
