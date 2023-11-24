import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from my_apps.shop.management.commands.set_database import Command
from my_apps.shop.models import Category, Product, Settings

fake = Faker()


@pytest.mark.django_db
def test_count_products():
    response = client.get("/api/v1/shop/product/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 96


client = APIClient()


@pytest.fixture(autouse=True)
def initialized_task_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    c = Command()
    c.create_categories()
    c.create_products()


@pytest.mark.django_db
def test_link_category():
    response = client.get("/api/v1/shop/guest_user/get_all_categories/")
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"error in get_all_categories, status: {response.status_code}"

    def testing_sub_categories(cat):
        for sub_cat in cat:
            url = sub_cat["url"]
            if sub_cat["icon"]:
                url = reverse("get_categories_foto", kwargs={"image_path": sub_cat["icon"][34:]})

                icon = client.get(url)
                assert icon.status_code == status.HTTP_200_OK, f"error in icon in category {url}"
            if sub_cat["img"]:
                url = reverse("get_categories_foto", kwargs={"image_path": sub_cat["img"][34:]})
                img = client.get(url)
                assert img.status_code == status.HTTP_200_OK, f"error in img in category {url}"
            assert len(sub_cat["url"]) > 1
            if sub_cat["sub"]:
                testing_sub_categories(sub_cat["sub"])

    testing_sub_categories(response.data)
