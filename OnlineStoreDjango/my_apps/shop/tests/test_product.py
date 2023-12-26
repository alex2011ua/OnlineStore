import pytest

from my_apps.shop.models import Product, Category
from django.urls import reverse
from rest_framework.test import APIClient
class TestProduct:
    @pytest.fixture()
    def initialize_task_db(self):
        category1 = Category.objects.create(name="category")
        product = Product.objects.create(
            name="Product", slug="Product", category=category1, price=10
        )
        return {"category1": category1, "product": product}

    @pytest.mark.django_db
    def test_get_product_by_id(self, initialize_task_db):
        product = initialize_task_db["product"]
        url = reverse("product-detail", kwargs={"pk": product.id})

        client = APIClient()
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == str(product.id)