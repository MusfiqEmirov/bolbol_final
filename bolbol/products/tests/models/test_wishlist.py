import pytest
from django.contrib.auth import get_user_model
from products.models import Product
from products.models.wishlist import Wishlist

User = get_user_model()

@pytest.mark.django_db
def test_wishlist_creation():
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0)
    
    wishlist_item = Wishlist.objects.create(user=user, product=product)
    
    assert wishlist_item.user == user
    assert wishlist_item.product == product
    assert wishlist_item.added_at is not None
    assert str(wishlist_item) == f"{user} - {product.name}"

@pytest.mark.django_db
def test_wishlist_unique_constraint():
    user = User.objects.create_user(phone_number="2222222222", password="testpass")
    product = Product.objects.create(name="Unique Product", owner=user, price=20.0)

    Wishlist.objects.create(user=user, product=product)
    
    with pytest.raises(Exception):  # IntegrityError olacaq duplicate üçün
        Wishlist.objects.create(user=user, product=product)

@pytest.mark.django_db
def test_wishlist_allows_null_user_or_product():
    # user və ya product null ola bilər, model bunu icazə verir.
    wishlist_item = Wishlist.objects.create(user=None, product=None)
    assert wishlist_item.user is None
    assert wishlist_item.product is None
