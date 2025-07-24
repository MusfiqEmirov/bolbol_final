import pytest
from django.contrib.auth import get_user_model
from products.models import Product, ComplaintCategory
from products.serializers import ComplaintCreateSerializer, ComplaintCategorySerializer

User = get_user_model()


@pytest.mark.django_db
def test_complaint_category_serializer():
    category = ComplaintCategory.objects.create(
        name="Delay",
        priority_level=1,
        description="Delayed delivery complaints"
    )
    
    serializer = ComplaintCategorySerializer(category)
    data = serializer.data

    assert "name" in data
    assert data["name"] == "Delay"
    assert "priority_level" not in data
    assert "description" not in data


@pytest.mark.django_db
def test_complaint_create_serializer():
    user = User.objects.create_user(
        phone_number="+994501234567",
        email="test@example.com",
        password="password123"
    )
    
    product = Product.objects.create(
        name="Test Product",
        owner=user,
        price=10.0
    )

    category = ComplaintCategory.objects.create(
        name="Quality Issue",
        priority_level=2,
        description="Quality related"
    )

    data = {
        "product": product.id,
        "category": category.id,
        "text": "The product was broken on arrival."
    }

    serializer = ComplaintCreateSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    complaint = serializer.save()
    assert complaint.product == product
    assert complaint.category == category
    assert complaint.text == "The product was broken on arrival."
