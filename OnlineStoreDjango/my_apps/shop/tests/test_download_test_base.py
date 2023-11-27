import pytest
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from django.core.management import call_command
from my_apps.shop.models import Category, Product, Settings
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@pytest.fixture(autouse=True, scope='session')
def initialized_task_db(django_db_setup, django_db_blocker):
    """Connect to db before testing, disconnect after."""
    with django_db_blocker.unblock():
        call_command("loaddata", "user.json")
        call_command("loaddata", "shop.json")


@pytest.mark.django_db
def test_count_products():
    response = client.get("/api/v1/shop/guest_user/search/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 96


client = APIClient()


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


@pytest.mark.django_db
def test_detail_product():
    p = Product.objects.all()[0]
    response = client.get(f"/api/v1/shop/guest_user/product/{p.pk}")
    assert response.status_code == 200
    assert "id" in response.data
    assert response.data["id"] == "1b82cdb5-916c-4af1-bd07-0ad08d4d5760"




