import pytest
from products.models import City
from products.serializers.city_serializer import CitySerializer


@pytest.mark.django_db
def test_city_serializer():
    city = City.objects.create(name="Baku")

    serializer = CitySerializer(city)
    data = serializer.data

    assert data["id"] == city.id
    assert data["name"] == "Baku"
