import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from my_apps.accounts.models import User
from my_apps.shop.api_v1.auth_user.auth_user_views import AuthComments
from my_apps.shop.api_v1.guest_user.guest_user_views import Comments
from my_apps.shop.models import Category, Product


class TestReviewProduct:
    @pytest.fixture()
    def init_task_db_review(self):
        category1 = Category.objects.create(name="cat1", slug="slugcat1")
        product1 = Product.objects.create(name="prod1", slug="prod1", category=category1, price=1)
        user_auth = User.objects.create(email="auth_user@gmail.com", role="U")
        return {"product": product1, "user": user_auth, "category": category1}

    @pytest.mark.django_db
    def test_product_review_get(self, init_task_db_review):
        factory = APIRequestFactory()
        product = init_task_db_review["product"]
        user = init_task_db_review["user"]
        request_get_reviews = factory.get(
            reverse("get_product_comments", kwargs={"prod_pk": product.id})
        )
        view_get_comment = Comments.as_view({"get": "list"})
        response = view_get_comment(request_get_reviews, prod_pk=product.id)

        assert response.data["count"] == 0
        # creating review
        product.reviews.create(author=user, title="test_title")
        response = view_get_comment(request_get_reviews, prod_pk=product.id)
        assert response.data["count"] == 1

    @pytest.mark.django_db
    def test_product_review_add(self, init_task_db_review):
        """test getting and creating review in product"""
        factory = APIRequestFactory()
        product = init_task_db_review["product"]
        count_prod = product.reviews.all().count()
        assert count_prod == 0
        user = init_task_db_review["user"]
        request_add_review = factory.post(
            reverse("auth_comments", kwargs={"pk": product.id}),
            {
                "text": "string1",
                "rate_by_stars": 2,
                "quality": 2,
                "description_match": "2",
                "photo_match": 2,
                "price": 2,
            },
        )
        # add new comment
        force_authenticate(request_add_review, user=user)
        view = AuthComments.as_view()
        response = view(request_add_review, pk=product.id)
        assert response.status_code == 200

        count_prod = product.reviews.all().count()
        assert count_prod == 1, "count comments should be 1"

        product = Product.objects.get(name="prod1")
        assert product.quality == 2, 'check correctly working signal "refresh_rating"'
        assert product._2 == 1 ,'check correctly working signal "refresh_rating"'

        request_add_review = factory.post(
            reverse("auth_comments", kwargs={"pk": product.id}),
            {
                "text": "string1",
                "rate_by_stars": 4,
                "quality": 4,
                "description_match": "4",
                "photo_match": 4,
                "price": 4,
            },
        )
        force_authenticate(request_add_review, user=user)
        view = AuthComments.as_view()
        response = view(request_add_review, pk=product.id)
        # add new comment
        product = Product.objects.get(name="prod1")
        assert product.quality == 3, 'check correctly working signal "refresh_rating"'
        assert product._2 == 1, 'check correctly working signal "refresh_rating"'
        assert product._4 == 1, 'check correctly working signal "refresh_rating"'