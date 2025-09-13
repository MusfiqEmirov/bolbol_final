import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from products.models import Product

User = get_user_model()


@pytest.mark.django_db
def test_active_products_count():
    user = baker.make(User)
    baker.make(
        Product,
        owner=user,
        is_active=True,
        name="Test Product",
        slug="test-product-1",
        _quantity=3,
    )
    assert user.products.filter(is_active=True).count() == 3

@pytest.mark.django_db
def test_create_user_with_phone():
    user = User.objects.create_user(phone_number="0501234567", password="secret")
    assert user.phone_number == "0501234567"
    assert user.check_password("secret")

@pytest.mark.django_db
def test_phone_number_is_unique():
    User.objects.create_user(phone_number="0501111111", password="secret")
    with pytest.raises(Exception):
        User.objects.create_user(phone_number="0501111111", password="another")

@pytest.mark.django_db
def test_get_masked_fullname():
    user = baker.make(User, full_name="Elvin Haxverdiyev")
    masked = user.get_masked_fullname()
    assert "*" in masked or masked != "Elvin Haxverdiyev"

@pytest.mark.django_db
def test_is_shop_profile_false_by_default():
    user = baker.make(User)
    assert user.is_shop_profile() is False

@pytest.mark.django_db
def test_active_products_count():
    user = baker.make(User)

    products = [
        baker.make(Product, owner=user, is_active=True, slug=f"active-{i}")
        for i in range(3)
    ]

    inactive = baker.make(Product, owner=user, is_active=False, slug="inactive-1")

    assert user.products.filter(is_active=True).count() == 3

