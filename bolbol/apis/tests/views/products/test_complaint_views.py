import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from products.models import ComplaintCategory, Complaint
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_complaint_category_list_api():
    # Bir neçə complaint category yaradaq
    ComplaintCategory.objects.create(name="Category 1")
    ComplaintCategory.objects.create(name="Category 2")

    client = APIClient()
    url = reverse("apis:complaint-category-list")
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Category 1" or data[1]["name"] == "Category 1"


@pytest.mark.django_db
def test_create_complaint_authenticated():
    user = User.objects.create_user(phone_number="1234567890", password="testpass")
    category = ComplaintCategory.objects.create(name="Category 1")

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("apis:complaint-create")
    data = {
        "category": category.id,
        "text": "This is a complaint text."
    }

    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["text"] == data["text"]
    assert Complaint.objects.filter(complainant=user, category=category).exists()


@pytest.mark.django_db
def test_create_complaint_unauthenticated():
    category = ComplaintCategory.objects.create(name="Category 1")

    client = APIClient()
    url = reverse("apis:complaint-create")
    data = {
        "category": category.id,
        "text": "This is a complaint text."
    }

    response = client.post(url, data)
    assert response.status_code == 401  # Unauthorized


