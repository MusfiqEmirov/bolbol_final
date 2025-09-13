import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import ProductPhoto
from products.models.product import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_product_photo(tmp_path):
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(name="Test Product", owner=user, price=10.0)

    image_content = b"fake-image-content"
    image_file = SimpleUploadedFile("test.jpg", image_content, content_type="image/jpeg")

    photo = ProductPhoto.objects.create(
        product=product,
        image=image_file,
        order=1
    )

    assert photo.product == product
    assert photo.order == 1
    # Fayl adında "test" var
    assert "test" in photo.image.name
    # .jpg ilə bitir
    assert photo.image.name.endswith(".jpg")
    assert str(photo) == f"{product} photo 1"


@pytest.mark.django_db
def test_get_image_url_returns_fixed_url():
    photo = ProductPhoto()
    url = photo.get_image_url()
    assert url == "https://konum24.az/uploads/products/photos/2025/02/04/2024-kia-sorento-facelift-3-200x200.jpg"
