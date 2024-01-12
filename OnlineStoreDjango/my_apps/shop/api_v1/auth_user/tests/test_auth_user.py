import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from my_apps.accounts.models import User
from my_apps.shop.api_v1.auth_user.auth_user_views import AuthComments
from my_apps.shop.api_v1.guest_user.guest_user_views import Comments
from my_apps.shop.models import Category, Product
from my_apps.shop.api_v1.auth_user.auth_user_views import Basket


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


