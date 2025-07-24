import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from products.models import Product, Category, City
from users.models import User
from products.serializers import (
    ProductCardSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer,
    ProductDeleteSerializer,
    ProductUpdateSerializer
)


@pytest.mark.django_db
def test_product_create_serializer_valid():
    user = User.objects.create_user(phone_number="+994500000000", password="testpassword123")
    category = Category.objects.create(name="Electronics")
    city = City.objects.create(name="Baku")

    data = {
        "name": "Test Product",
        "category": category.id,
        "city": city.id,
        "price": 100.0,
        "description": "Test description",
        "is_new_product": True,
        "is_delivery_available": True,
        "is_credit_available": False,
        "is_barter_available": False,
        "is_via_negotiator": False,
        "characteristics": {"color": "red", "size": "M"}
    }

    serializer = ProductCreateSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    product = serializer.save(owner=user)
    assert product.name == "Test Product"
    assert product.city == city
    assert product.category == category


@pytest.mark.django_db
def test_product_update_serializer_valid():
    category = Category.objects.create(name="Updated")
    city = City.objects.create(name="Ganja")

    user = User.objects.create_user(phone_number="+994500000001", password="testpassword123")
    product = Product.objects.create(
        owner=user,
        name="Old Product",
        category=category,
        city=city,
        price=50,
        description="Old desc",
        is_new_product=False,
        is_delivery_available=False,
        is_credit_available=False,
        is_barter_available=False,
        is_via_negotiator=False,
        characteristics={"old": "value"}
    )

    updated_data = {
        "name": "Updated Product",
        "category": category.id,
        "city": city.id,
        "price": 99.9,
        "description": "Updated desc",
        "is_new_product": True,
        "is_delivery_available": True,
        "is_credit_available": True,
        "is_barter_available": False,
        "is_via_negotiator": True,
        "characteristics": {"new": "updated"}
    }

    serializer = ProductUpdateSerializer(product, data=updated_data)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.name == "Updated Product"
    assert updated.characteristics["new"] == "updated"


@pytest.mark.django_db
def test_product_delete_serializer_valid_ids():
    user = User.objects.create_user(phone_number="+994500000002", password="testpassword123")
    product1 = Product.objects.create(owner=user, name="P1", price=10)
    product2 = Product.objects.create(owner=user, name="P2", price=20)

    request = APIRequestFactory().post("/")
    request.user = user

    serializer = ProductDeleteSerializer(
        data={"ids": [product1.id, product2.id]},
        context={"request": request}
    )
    assert serializer.is_valid(), serializer.errors
    assert set(serializer.validated_data["ids"]) == {product1.id, product2.id}


@pytest.mark.django_db
def test_product_delete_serializer_invalid_ids():
    user = User.objects.create_user(phone_number="+994500000003", password="testpassword123")
    another_user = User.objects.create_user(phone_number="+994500000004", password="testpassword123")

    product = Product.objects.create(owner=another_user, name="Other's product", price=30)

    request = APIRequestFactory().post("/")
    request.user = user

    serializer = ProductDeleteSerializer(
        data={"ids": [product.id]},
        context={"request": request}
    )
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)
    assert "do not belong to you" in str(e.value)
