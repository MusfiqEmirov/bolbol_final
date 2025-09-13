import pytest
from django.contrib.auth import get_user_model
from products.models import Product
from products.models.moderation_requests import ProductUpdateRequest, ReactivationRequest  # faylın yerləşməsinə uyğun düzəliş et

User = get_user_model()

@pytest.mark.django_db
def test_create_product_update_request():
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    product = Product.objects.create(
        name="Test Product",
        owner=user,
        price=10.0,  # burada price əlavə et
    )

    update_data = {"price": 100, "description": "Updated description"}
    user_data = {"name": "John Doe"}
    photo_meta = {"photo_count": 3}

    update_request = ProductUpdateRequest.objects.create(
        product=product,
        data=update_data,
        user_data=user_data,
        photo_meta=photo_meta,
        status=ProductUpdateRequest.PENDING,
    )

    assert update_request.product == product
    assert update_request.data == update_data
    assert update_request.user_data == user_data
    assert update_request.photo_meta == photo_meta
    assert update_request.status == ProductUpdateRequest.PENDING
    assert update_request.reviewed_at is None
    assert update_request.reviewed_by is None


@pytest.mark.django_db
def test_create_reactivation_request():
    user = User.objects.create_user(phone_number="0987654321", password="testpass")
    product = Product.objects.create(
        name="Test Product 2",
        owner=user,
        price=15.0,  # price əlavə et
    )

    reactivation_request = ReactivationRequest.objects.create(
        product=product,
        user=user,
        status=ReactivationRequest.PENDING,
        admin_note="Initial request"
    )

    assert reactivation_request.product == product
    assert reactivation_request.user == user
    assert reactivation_request.status == ReactivationRequest.PENDING
    assert reactivation_request.admin_note == "Initial request"
    assert reactivation_request.created_at is not None
    assert str(reactivation_request) == f"Reactivation request for {product} by {user}"


@pytest.mark.django_db
def test_reactivation_request_status_choices():
    user = User.objects.create_user(phone_number="1234509876", password="testpass")
    product = Product.objects.create(
        name="Test Product 3",
        owner=user,
        price=20.0,  # price əlavə et
    )

    request = ReactivationRequest.objects.create(product=product, user=user)

    request.status = ReactivationRequest.APPROVED
    request.save()
    assert request.status == ReactivationRequest.APPROVED

    request.status = ReactivationRequest.REJECTED
    request.save()
    assert request.status == ReactivationRequest.REJECTED
