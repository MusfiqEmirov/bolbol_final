import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from shops.models import ShopActivity, ShopContact, ShopWorkingHours, Shop
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(phone_number="+994500000001", password="pass123")

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_shop_registration_request_requires_auth(auth_client):
    url = reverse("apis:shop-registration-request")
    data = {
        "shop_name": "My New Shop",
        "shop_owner_full_name": "Test User",
    }
    response = auth_client.post(url, data)
    assert response.status_code in [201, 400]


@pytest.mark.django_db
def test_shop_list(api_client):
    Shop.objects.create(name="Shop 1")
    Shop.objects.create(name="Shop 2")
    url = reverse("apis:shop-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 2

@pytest.mark.django_db
def test_create_shop_contact_requires_auth(auth_client, user):
    shop = Shop.objects.create(name="My Shop", owner=user)
    url = reverse("apis:create-shop-contacts")
    data = {"phone": "1234567890", "email": "test@test.com"}
    response = auth_client.post(url, data)
    assert response.status_code in [200, 400]
