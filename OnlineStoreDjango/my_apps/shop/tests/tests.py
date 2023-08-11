import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from my_apps.shop.models import Category, Product, Settings

fake = Faker()
client = APIClient()


@pytest.mark.django_db
def test_list_popular_gifts_true():
    category = Category.objects.create(name="cat1", slug="slugcat1")
    slug = [fake.unique.first_name() for i in range(11)]
    # create 10 products with different rating and counts of sailing
    for i in range(11):
        Product.objects.create(
            name=fake.name(),
            slug=slug[i],
            category=category,
            price=i,
            quantity=i,
            sold=i,
            global_rating=i,
        )
    # get rating limit from DB
    rate_limit, _ = Settings.objects.get_or_create(
        name="rate_limit",
        defaults={"description": "show gifts with rate more then value", "value": 6},
    )

    # get list of most popular products with rate more than ate_limit.value
    response = client.get(f"/api/v1/shop/na/popular/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 10 - rate_limit.value
