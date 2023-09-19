import pytest
from django.shortcuts import redirect
from rest_framework.test import APIRequestFactory, force_authenticate

from my_apps.accounts.models import User
from my_apps.shop.models import Category, Product

from .auth_user_views import Basket


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

    request = factory.get(redirect("basket"))
    force_authenticate(request, user=user)
    response = view(request)
    assert response.data["products"] == []

    p = Product.objects.all()[0]
    request = factory.post(redirect("basket"), {"product": p.id, "amount": 2})
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 201

    request = factory.get(redirect("basket"))
    force_authenticate(request, user=user)
    response = view(request)
    assert response.data["products"] != []
    assert len(response.data["products"]) == 1
