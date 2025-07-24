import pytest
from rest_framework.test import APIClient
from products.models import City

@pytest.mark.django_db
def test_city_list_api_view_returns_active_cities():
    client = APIClient()

    active_city1 = City.objects.create(name="Active City 1", is_active=True, order=1)
    active_city2 = City.objects.create(name="Active City 2", is_active=True, order=2)
    inactive_city = City.objects.create(name="Inactive City", is_active=False, order=3)

    response = client.get("/api/v1/cities/")

    assert response.status_code == 200
    data = response.json()

    returned_city_names = {city["name"] for city in data}
    assert active_city1.name in returned_city_names
    assert active_city2.name in returned_city_names
    assert inactive_city.name not in returned_city_names
    assert len(data) == 2
