import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

@pytest.mark.django_db
def test_user_detail_api_view_not_found():
    client = APIClient()
    url = reverse("apis:user-detail", kwargs={"pk": 999999})  
    response = client.get(url)

    assert response.status_code == 404
    assert "error" in response.data


@pytest.mark.django_db
def test_user_update_api_view_unauthenticated():
    client = APIClient()
    url = reverse("apis:user-update")
    response = client.patch(url, {}, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_product_card_list_by_user_api_view():
    user = baker.make(User)
    active_products = [baker.make(Product, owner=user, is_active=True, slug=f"test-slug-{i}") for i in range(3)]
    inactive_product = baker.make(Product, owner=user, is_active=False, slug="inactive-slug")

    client = APIClient()
    url = reverse("apis:user-product-cards", kwargs={"user_id": user.id})

    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

    category = baker.make("products.Category")
    active_products[0].category = category
    active_products[0].save()

    response = client.get(url, {"category_id": category.id})
    assert response.status_code == 200
    assert len(response.data) == 1



@pytest.mark.django_db
def test_user_product_status_list_api_view():
    user = baker.make(User)
    approved_active = baker.make(Product, owner=user, status=Product.APPROVED, is_active=True, slug="approved-active")
    pending_active = baker.make(Product, owner=user, status=Product.PENDING, is_active=True, slug="pending-active")
    approved_inactive = baker.make(Product, owner=user, status=Product.APPROVED, is_active=False, slug="approved-inactive")

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("apis:user-product-statuses", kwargs={"user_id": user.id})

    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

