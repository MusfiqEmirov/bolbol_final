import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from products.models import Product, ReactivationRequest, ProductUpdateRequest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_product_create_api_with_photos(tmp_path):
    user = User.objects.create_user(phone_number="1234567890", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)

    # Create dummy image files for upload
    image1 = tmp_path / "image1.jpg"
    image1.write_bytes(b"fakeimagecontent1")
    image2 = tmp_path / "image2.jpg"
    image2.write_bytes(b"fakeimagecontent2")

    url = reverse("apis:product-create")

    data = {
        "name": "Test Product",
        "price": "99.99",
        "slug": "test-product",
        "is_active": True,
        "owner": json.dumps({"full_name": "Test User", "email": "test@example.com"}),
        "photos": [
            open(image1, "rb"),
            open(image2, "rb"),
        ],
    }

    response = client.post(url, data, format="multipart")

    # Close files
    for f in data["photos"]:
        f.close()

    assert response.status_code == 201
    product = Product.objects.filter(name="Test Product", owner=user).first()
    assert product is not None
    # Ensure photos are linked to product
    assert product.photos.count() == 2

@pytest.mark.django_db
def test_request_product_reactivation_api():
    user = User.objects.create_user(phone_number="1234567890", password="pass")
    product = Product.objects.create(
        owner=user,
        name="Inactive Product",
        slug=f"{1}-inactive-product",  # burada id-ni düz yaz, 1 deyil, product.id
        price=50,
        is_active=False,
    )
    # düzgün slug yaratmaq üçün
    product.slug = f"{product.id}-inactive-product"
    product.save()

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("apis:reactivation-product", kwargs={"product_slug": product.slug})

    # First request should succeed
    response1 = client.post(url)
    assert response1.status_code == 201
    assert ReactivationRequest.objects.filter(product=product, user=user).exists()

    # Duplicate request should fail
    response2 = client.post(url)
    assert response2.status_code == 400

    # Active product should return 400
    product.is_active = True
    product.save()
    response3 = client.post(url)
    assert response3.status_code == 400

@pytest.mark.django_db
def test_bulk_delete_products_api():
    user = User.objects.create_user(phone_number="1234567890", password="pass")
    products = [
        Product.objects.create(owner=user, name=f"Product {i}", slug=f"slug-{i}", price=10 * i, is_active=True)
        for i in range(3)
    ]
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("apis:bulk-delete-products")
    data = {"ids": [p.id for p in products]}
    response = client.delete(url, data, format="json")

    assert response.status_code == 200
    assert Product.objects.filter(id__in=[p.id for p in products]).count() == 0
    assert response.json()["message"].startswith("3 product")

@pytest.mark.django_db
def test_product_update_request_api(tmp_path):
    user = User.objects.create_user(phone_number="1234567890", password="pass")
    product = Product.objects.create(
        owner=user,
        name="Active Product",
        slug="active-product",
        price=100,
        is_active=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("apis:product-update-request", kwargs={"product_slug": product.slug})

    # Create dummy image files for upload
    image = tmp_path / "image.jpg"
    image.write_bytes(b"fakeimagecontent")

    data = {
        "name": "Updated Product Name",
        "price": "110",
        "owner": json.dumps({"full_name": "Updated User", "email": "updated@example.com"}),
        "photos": [open(image, "rb")],
    }

    response = client.post(url, data, format="multipart")

    # Close file
    for f in data["photos"]:
        f.close()

    assert response.status_code == 202
    assert ProductUpdateRequest.objects.filter(product=product, status=ProductUpdateRequest.PENDING).exists()

@pytest.mark.django_db
def test_product_update_request_duplicate_pending():
    user = User.objects.create_user(phone_number="1234567890", password="pass")
    product = Product.objects.create(owner=user, name="Product", slug="product", price=100, is_active=True)

    # İlk ProductUpdateRequest yaradılır
    ProductUpdateRequest.objects.create(
        product=product,
        status=ProductUpdateRequest.PENDING,
        data={},  # boş dict əlavə edilir
    )

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("apis:product-update-request", kwargs={"product_slug": product.slug})

    # Eyni məhsul üçün ikinci update request göndərmək istəyəndə xəta olmalıdır
    response = client.post(url)
    assert response.status_code == 400

    # Status PENDING olan başqa update request olmadan yenisi uğurla yaradılmalıdır
    # (Burada əlavə yoxlama üçün əvvəlki PENDING silinir)
    ProductUpdateRequest.objects.all().delete()

    response2 = client.post(url)
    assert response2.status_code == 202

    assert ProductUpdateRequest.objects.filter(product=product, status=ProductUpdateRequest.PENDING).exists()

@pytest.mark.django_db
def test_product_update_request_inactive_or_expired():
    user = User.objects.create_user(phone_number="1234567890", password="pass")

    # Inactive product
    product1 = Product.objects.create(owner=user, name="Prod1", slug="prod1", price=10, is_active=False)
    client = APIClient()
    client.force_authenticate(user=user)
    url1 = reverse("apis:product-update-request", kwargs={"product_slug": product1.slug})

    response1 = client.post(url1, {"owner": json.dumps({})}, format="multipart")
    assert response1.status_code == 400
    assert "not active" in response1.json().get("error", "").lower()

    # Expired product
    from django.utils import timezone
    import datetime
    product2 = Product.objects.create(
        owner=user, name="Prod2", slug="prod2", price=10, is_active=True,
        expires_at=timezone.now() - datetime.timedelta(days=1)
    )
    url2 = reverse("apis:product-update-request", kwargs={"product_slug": product2.slug})
    response2 = client.post(url2, {"owner": json.dumps({})}, format="multipart")
    assert response2.status_code == 400
    assert "expired" in response2.json().get("error", "").lower()
