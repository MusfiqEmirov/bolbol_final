import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from products.models import Product, Wishlist
from django.contrib.auth import get_user_model

User = get_user_model()  # İstifadəçi modelini düzgün alırıq


@pytest.mark.django_db
def test_get_empty_wishlist():
    user = User.objects.create_user(phone_number="1234567890", password="pass1234")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("apis:bookmark")  # Düz URL adı

    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_add_product_to_wishlist():
    user = User.objects.create_user(phone_number="1234567890", password="pass1234")
    product = Product.objects.create(
        owner=user,
        name="Test Product",
        slug="test-product",
        price=100,
        is_active=True,
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("apis:bookmark")

    response = client.post(url, data={"product_id": product.id}, format="json")
    assert response.status_code == 201
    assert response.json()["status"] == "added"
    assert Wishlist.objects.filter(user=user, product=product).exists()


@pytest.mark.django_db
def test_remove_product_from_wishlist():
    user = User.objects.create_user(phone_number="1234567890", password="pass1234")
    product = Product.objects.create(
        owner=user,
        name="Test Product",
        slug="test-product",
        price=100,
        is_active=True,
    )
    Wishlist.objects.create(user=user, product=product)

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("apis:bookmark")

    response = client.post(url, data={"product_id": product.id}, format="json")
    assert response.status_code == 200
    assert response.json()["status"] == "removed"
    assert not Wishlist.objects.filter(user=user, product=product).exists()


@pytest.mark.django_db
def test_post_without_product_id_returns_400():
    user = User.objects.create_user(phone_number="1234567890", password="pass1234")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("apis:bookmark")

    response = client.post(url, data={}, format="json")
    assert response.status_code == 400
    assert "error" in response.json()
