import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from products.models import Product
from utils.helpers import shrink_text
from products.models.product_photo import ProductPhoto
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.mark.django_db
def test_create_product_photo(tmp_path):
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0)

    # Fake image file
    image_content = b"fake-image-content"
    image_file = SimpleUploadedFile("test.jpg", image_content, content_type="image/jpeg")

    photo = ProductPhoto.objects.create(
        product=product,
        image=image_file,
        order=1
    )

    assert photo.product == product
    assert photo.order == 1
    # Faylın .jpg ilə bitdiyini yoxlayırıq
    assert photo.image.name.endswith(".jpg")
    # Fayl adında "test" kəlməsi var
    assert "test" in photo.image.name



@pytest.mark.django_db
def test_str_method_returns_shortened_name():
    user = User.objects.create_user(phone_number="2222222222", password="testpass")
    long_name = "A" * 50
    product = Product.objects.create(
        name=long_name,
        owner=user,
        price=200.0,
    )
    expected = shrink_text(long_name, 25)
    assert str(product) == expected

@pytest.mark.django_db
def test_get_absolute_url_returns_correct_url():
    user = User.objects.create_user(phone_number="3333333333", password="testpass")
    product = Product.objects.create(
        name="Product 3",
        owner=user,
        price=300.0,
        slug="product-3"
    )
    url = product.get_absolute_url()
    assert "product-3" in url
    # Əlavə yoxlama: URL `apis:product-detail` adlandırılan yol olmalıdır

@pytest.mark.django_db
def test_deactivate_sets_is_active_false():
    user = User.objects.create_user(phone_number="4444444444", password="testpass")
    product = Product.objects.create(
        name="Product 4",
        owner=user,
        price=400.0,
        is_active=True
    )
    product.deactivate()
    product.refresh_from_db()
    assert product.is_active is False

@pytest.mark.django_db
def test_product_flags_defaults():
    user = User.objects.create_user(phone_number="5555555555", password="testpass")
    product = Product.objects.create(
        name="Product 5",
        owner=user,
        price=500.0
    )
    assert product.is_new_product is False
    assert product.is_delivery_available is False
    assert product.is_credit_available is False
    assert product.is_barter_available is False
    assert product.is_via_negotiator is False
    assert product.is_vip is False
    assert product.is_premium is False
    assert product.is_promoted is False
    assert product.is_super_chance is False
