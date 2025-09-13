import pytest
from shops.models import ShopRegistrationRequest, ShopActivity, Shop
from users.models import User


@pytest.mark.django_db
def test_create_shop_registration_request_minimal():
    user = User.objects.create_user(phone_number="+994500000005", password="password123")
    activity = ShopActivity.objects.create(name="Retail")
    request = ShopRegistrationRequest.objects.create(
        shop_owner=user,
        shop_owner_full_name="John Doe",
        shop_name="John's Store",
    )
    request.shop_activities.add(activity)
    assert request.id is not None
    assert request.status == ShopRegistrationRequest.IN_REVIEW
    assert activity in request.shop_activities.all()


@pytest.mark.django_db
def test_str_method_returns_shop_name():
    user = User.objects.create_user(phone_number="+994500000010", password="password123")
    request = ShopRegistrationRequest.objects.create(shop_owner=user, shop_name="My Shop")
    assert str(request) == "My Shop"


@pytest.mark.django_db
def test_default_status_is_in_review():
    user = User.objects.create_user(phone_number="+994500000011", password="password123")
    request = ShopRegistrationRequest.objects.create(shop_owner=user, shop_name="Shop A")
    assert request.status == ShopRegistrationRequest.IN_REVIEW


@pytest.mark.django_db
def test_save_does_not_create_shop_if_already_exists():
    user = User.objects.create_user(phone_number="+994500000007", password="password123")
    existing_shop = Shop.objects.create(owner=user, name="Existing Shop", is_active=True)
    request = ShopRegistrationRequest(
        shop_owner=user,
        shop_name="Existing Shop Request",
        status=ShopRegistrationRequest.APPROVED,
    )
    request.save()
    shop_count = Shop.objects.filter(owner=user, is_active=True).count()
    assert shop_count == 1 


@pytest.mark.django_db
def test_status_can_be_changed():
    user = User.objects.create_user(phone_number="+994500000012", password="password123")
    request = ShopRegistrationRequest.objects.create(shop_owner=user, shop_name="Shop B")
    request.status = ShopRegistrationRequest.APPROVED
    request.save()
    updated = ShopRegistrationRequest.objects.get(id=request.id)
    assert updated.status == ShopRegistrationRequest.APPROVED


@pytest.mark.django_db
def test_shop_activities_many_to_many():
    user = User.objects.create_user(phone_number="+994500000013", password="password123")
    request = ShopRegistrationRequest.objects.create(shop_owner=user, shop_name="Multi Activity Shop")
    activity1 = ShopActivity.objects.create(name="Activity 1")
    activity2 = ShopActivity.objects.create(name="Activity 2")
    request.shop_activities.add(activity1, activity2)
    assert request.shop_activities.count() == 2


@pytest.mark.django_db
def test_created_at_and_updated_at_auto_set():
    user = User.objects.create_user(phone_number="+994500000014", password="password123")
    request = ShopRegistrationRequest.objects.create(shop_owner=user, shop_name="Timestamps Shop")
    assert request.created_at is not None
    assert request.updated_at is not None


@pytest.mark.django_db
def test_updated_at_changes_on_save():
    user = User.objects.create_user(phone_number="+994500000015", password="password123")
    request = ShopRegistrationRequest.objects.create(shop_owner=user, shop_name="Update Time Shop")
    old_updated_at = request.updated_at
    request.shop_name = "Changed Shop Name"
    request.save()
    request.refresh_from_db()
    assert request.updated_at > old_updated_at