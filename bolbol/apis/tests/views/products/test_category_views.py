import pytest
from rest_framework.test import APIClient
from products.models import Category

@pytest.mark.django_db
def test_category_api_view_returns_parent_categories():
    client = APIClient()

    parent_category = Category.objects.create(name="Parent Category", is_active=True, parent_category=None)
    sub_category = Category.objects.create(name="Sub Category", is_active=True, parent_category=parent_category)
    inactive_category = Category.objects.create(name="Inactive Category", is_active=False, parent_category=None)

    response = client.get("/api/v1/categories/")  # Əgər api prefix varsa

    assert response.status_code == 200
    data = response.json()

    # Yalnız aktiv və parent_category__isnull=True olanlar gəlməlidir
    assert any(cat['id'] == parent_category.id for cat in data)
    assert all('parent_category' not in cat or cat['parent_category'] is None for cat in data)
    assert all(cat['is_active'] for cat in data)
