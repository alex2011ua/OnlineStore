import pytest
from django.urls import reverse
from faker import Faker
from my_apps.shop.models import Category, Product, Settings
from rest_framework import status
from rest_framework.test import APIClient

fake = Faker()
client = APIClient()


@pytest.fixture(autouse=True)
def initialized_task_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    category1 = Category.objects.create(name="cat1", slug="slugcat1")


@pytest.mark.django_db
def test_list_popular_gifts_true():
    category = Category.objects.get()
    slug = [fake.unique.first_name() for i in range(11)]
    # create 10 products with different rating and counts of sailing
    for i in range(11):
        Product.objects.create(
            name=fake.name(),
            slug=slug[i],
            category=category,
            price=i+1,
            quantity=i,
            sold=i,
            global_rating=i,
        )

    # get list of most popular products with rate more than ate_limit.value
    response = client.get("/api/v1/shop/guest_user/search/", {"rate": 4})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 10 - 3


@pytest.mark.django_db
def test_list_search_gifts():
    category = Category.objects.get()
    product1 = Product.objects.create(
        name="product1", slug="slug_prod1", category=category, price=10.00
    )
    product2 = Product.objects.create(
        name="product2", slug="slug_prod2", category=category, price=10.00
    )
    product3 = Product.objects.create(
        name="lsd", slug="product2", category=category, price=10.00
    )
    product4 = Product.objects.create(
        name="cat1", slug="nomater1", category=category, price=10.00
    )
    product5 = Product.objects.create(
        name="pcat2", slug="nomater2", category=category, price=10.00
    )
    product6 = Product.objects.create(
        name="something", slug="other", category=category, price=10.00
    )

    url = reverse("search")
    response = client.get(url, {"search": "product"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3


@pytest.mark.django_db
def test_list_new_gifts():
    category = Category.objects.get()
    p_first = Product.objects.create(
        name="product1", slug="slug_1", category=category, price=10.00
    )

    p_third = Product.objects.create(
        name="product3", slug="slug_3", category=category, price=10.00
    )

    p_second = Product.objects.create(
        name="product2", slug="slug_2", category=category, price=10.00
    )
    url = reverse("search")
    response = client.get(url, {"sort": "new"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3
    assert response.data["results"][0]["name"] == "product2"
