import pytest
from products.models import Category
from products.serializers.category_serializer import CategorySerializer, SubcategorySerializer


@pytest.mark.django_db
def test_category_serializer_with_subcategories():
    parent = Category.objects.create(name="Electronics", is_active=True)
    sub1 = Category.objects.create(name="Phones", parent_category=parent, is_active=True)
    sub2 = Category.objects.create(name="Laptops", parent_category=parent, is_active=True)
    Category.objects.create(name="Hidden", parent_category=parent, is_active=False) 

    serializer = CategorySerializer(parent)
    data = serializer.data

    assert data["id"] == parent.id
    assert data["name"] == "Electronics"
    assert "parent_category_id" not in data or data["parent_category_id"] is None
    assert len(data["subcategories"]) == 2
    assert {sub["name"] for sub in data["subcategories"]} == {"Phones", "Laptops"}


@pytest.mark.django_db
def test_subcategory_serializer():
    parent = Category.objects.create(name="Vehicles", is_active=True)
    sub = Category.objects.create(name="Bikes", parent_category=parent, is_active=True)

    # mocking the method get_category_based_products_count
    sub.get_category_based_products_count = 5

    serializer = SubcategorySerializer(sub)
    data = serializer.data

    assert data["id"] == sub.id
    assert data["name"] == "Bikes"
    assert data["parent_category_id"] == parent.id
    assert data["products_count"] == 5
