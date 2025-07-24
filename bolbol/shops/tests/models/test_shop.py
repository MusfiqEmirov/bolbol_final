import pytest
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import City, Product
from shops.models import Shop, ShopContact, ShopWorkingHours
from users.models import User


@pytest.mark.django_db
def test_create_shop_minimal():
    user = User.objects.create_user(phone_number="+994500000000", password="testpass")
    city = City.objects.create(name="Baku")
    shop = Shop.objects.create(owner=user, name="Test Shop", city=city)
    assert shop.id is not None
    assert shop.name == "Test Shop"
    assert shop.city == city
    assert shop.owner == user
    assert shop.is_active is True  


@pytest.mark.django_db
def test_shop_get_product_count_property():
    user = User.objects.create_user(phone_number="+994500000001", password="testpass")
    shop = Shop.objects.create(owner=user, name="Shop 1")
    # Create active and inactive products
    Product.objects.create(owner=user, name="Product 1", price=10, is_active=True)
    Product.objects.create(owner=user, name="Product 2", price=15, is_active=False)
    assert shop.get_product_count == 1


@pytest.mark.django_db
def test_shop_str_method():
    user = User.objects.create_user(phone_number="+994500000003", password="testpass")
    shop = Shop.objects.create(owner=user, name="My Shop")
    assert str(shop) == "My Shop"


@pytest.mark.django_db
def test_create_shop_contact_and_str():
    user = User.objects.create_user(phone_number="+994500000004", password="testpass")
    shop = Shop.objects.create(owner=user, name="Shop with Contact")
    contact = ShopContact.objects.create(shop=shop, phone_number="+994123456789")
    assert contact.shop == shop
    assert str(contact) == "+994123456789"


@pytest.mark.django_db
def test_shop_contact_phone_number_optional():
    user = User.objects.create_user(phone_number="+994500000005", password="testpass")
    shop = Shop.objects.create(owner=user, name="Shop Contact Optional")
    contact = ShopContact.objects.create(shop=shop, phone_number=None)
    assert contact.phone_number is None


@pytest.mark.django_db
def test_unique_together_shop_day_of_week():
    user = User.objects.create_user(phone_number="+994500000007", password="testpass")
    shop = Shop.objects.create(owner=user, name="Shop Unique Day")
    ShopWorkingHours.objects.create(shop=shop, day_of_week="Tuesday", opening_time="09:00", closing_time="17:00")
    with pytest.raises(Exception):  
        ShopWorkingHours.objects.create(shop=shop, day_of_week="Tuesday", opening_time="10:00", closing_time="18:00")


@pytest.mark.django_db
def test_shop_logo_and_background_image_upload():
    user = User.objects.create_user(phone_number="+994500000008", password="testpass")
    shop = Shop.objects.create(owner=user, name="Shop With Images")

    logo = SimpleUploadedFile("logo.png", b"fake-image-content", content_type="image/png")
    bg = SimpleUploadedFile("bg.png", b"fake-bg-content", content_type="image/png")

    shop.logo = logo
    shop.background_image = bg
    shop.save()
    shop.refresh_from_db()
    assert shop.logo.name.startswith("shops/logos/")
    assert shop.background_image.name.startswith("shops/background/")
