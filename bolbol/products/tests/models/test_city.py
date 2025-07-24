import pytest
from products.models import City

@pytest.mark.django_db
def test_city_creation_and_str():
    city = City.objects.create(
        name="Bakı",
        is_active=True,
        is_pinned=True,
        order=1
    )
    assert city.name == "Bakı"
    assert city.is_active is True
    assert city.is_pinned is True
    assert city.order == 1
    assert str(city) == "Bakı"

@pytest.mark.django_db
def test_city_ordering():
    city1 = City.objects.create(name="Gəncə", is_pinned=False, order=2)
    city2 = City.objects.create(name="Sumqayıt", is_pinned=True, order=1)
    cities = list(City.objects.all())
    # Ordering ("is_pinned", "order") — is_pinned = False < True, ona görə belə sıralanır
    assert cities[0] == city1
    assert cities[1] == city2

@pytest.mark.django_db
def test_city_unique_order_constraint():
    City.objects.create(name="Şəki", order=5)
    with pytest.raises(Exception):
        # İkinci city eyni order ilə yaradılmağa çalışılsa, unique constraint pozulacaq
        City.objects.create(name="Lənkəran", order=5)
