import pytest
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from rest_framework.exceptions import ValidationError
from products.models import Product
from products.serializers import (
    ProductDeleteSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
)

User = get_user_model()
factory = RequestFactory()


@pytest.mark.django_db
def test_product_create_serializer_valid_data():
    data = {
        "name": "New Product",
        "category": None,
        "city": None,
        "price": 100,
        "description": "A product description",
        "is_new_product": True,
        "is_delivery_available": True,
        "is_credit_available": False,
        "is_barter_available": False,
        "is_via_negotiator": True,
        "characteristics": {},
    }
    serializer = ProductCreateSerializer(data=data)
    assert serializer.is_valid(), serializer.errors