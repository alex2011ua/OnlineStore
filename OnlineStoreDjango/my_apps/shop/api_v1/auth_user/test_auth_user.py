import logging
import sys

import pytest
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from my_apps.accounts.models import User
from my_apps.shop.api_v1.auth_user.auth_user_views import AuthComments
from my_apps.shop.api_v1.guest_user.guest_user_views import Comments
from my_apps.shop.models import Category, Product

from .auth_user_views import Basket


@pytest.fixture()
def initalized_task_db():
    category1 = Category.objects.create(name="cat1", slug="slugcat1")
    product1 = Product.objects.create(name="prod1", slug="prod1", category=category1, price=1)
    user_auth = User.objects.create(email="auth_user@gmail.com", role="U")
    return {"user": user_auth, "product": product1, "category": category1}


@pytest.mark.django_db
def test_basket_endpoints(initalized_task_db):
    factory = APIRequestFactory()
    user = User.objects.get(email="auth_user@gmail.com")
    view = Basket.as_view()

    request = factory.get(reverse("auth_user_basket"))
    force_authenticate(request, user=user)
    response = view(request)
    assert response.data == []

    p = Product.objects.all()[0]
    request = factory.post(reverse("auth_user_basket"), {"product_id": p.id, "amount": 2})
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200

    request = factory.get(reverse("auth_user_basket"))
    force_authenticate(request, user=user)
    response = view(request)
    assert response.data != []
    assert len(response.data) == 1


class TestReviewProduct:
    @pytest.fixture()
    def initalized_task_db_review(self):
        category1 = Category.objects.create(name="cat1", slug="slugcat1")
        product1 = Product.objects.create(name="prod1", slug="prod1", category=category1, price=1)
        user_auth = User.objects.create(email="auth_user@gmail.com", role="U")
        return {"product": product1, "user": user_auth, "category": category1}

    @pytest.mark.django_db
    def test_product_review_get(self, initalized_task_db_review):
        factory = APIRequestFactory()
        product = initalized_task_db_review["product"]
        user = initalized_task_db_review["user"]
        request_get_reviews = factory.get(reverse("get_product_comments", kwargs={"prod_pk": product.id}))
        view_get_comment = Comments.as_view({"get": "list"})
        response = view_get_comment(request_get_reviews, prod_pk=product.id)

        assert response.data["count"] == 0
        # creating review
        product.reviews.create(author=user, title="test_title")
        response = view_get_comment(request_get_reviews, prod_pk=product.id)
        assert response.data["count"] == 1

    @pytest.mark.django_db
    def test_product_review_add(self, initalized_task_db_review):
        """test getting and creating review in product"""
        factory = APIRequestFactory()
        product = initalized_task_db_review["product"]
        count_prod = product.reviews.all().count()
        assert count_prod == 0
        user = initalized_task_db_review["user"]
        request_add_review = factory.post(
            reverse("auth_comments", kwargs={"pk": product.id}),
            {"title": "string", "text": "string"},
        )
        # add new comment
        force_authenticate(request_add_review, user=user)
        view = AuthComments.as_view()
        response = view(request_add_review, pk=product.id)
        assert response.status_code == 200
        # count comments should be 1
        count_prod = product.reviews.all().count()
        assert count_prod == 1
