import pytest
from shops.models import ShopActivity

@pytest.mark.django_db
def test_create_shop_activity_minimal():
    activity = ShopActivity.objects.create(name="Activity 1")
    assert activity.id is not None
    assert activity.name == "Activity 1"
    assert activity.is_active is True

@pytest.mark.django_db
def test_create_shop_activity_with_is_active_false():
    activity = ShopActivity.objects.create(name="Inactive Activity", is_active=False)
    assert activity.is_active is False

@pytest.mark.django_db
def test_name_field_max_length():
    long_name = "a" * 64
    activity = ShopActivity.objects.create(name=long_name)
    assert activity.name == long_name
    assert len(activity.name) <= 64

@pytest.mark.django_db
def test_name_field_allows_null_and_blank():
    activity = ShopActivity.objects.create(name=None)
    assert activity.name is None

    activity2 = ShopActivity.objects.create(name="")
    assert activity2.name == ""

@pytest.mark.django_db
def test_unique_name_constraint():
    ShopActivity.objects.create(name="Unique Activity")
    with pytest.raises(Exception): 
        ShopActivity.objects.create(name="Unique Activity")

@pytest.mark.django_db
def test_str_method_returns_name():
    activity = ShopActivity.objects.create(name="Test Activity")
    assert str(activity) == "Test Activity"

@pytest.mark.django_db
def test_update_shop_activity_name():
    activity = ShopActivity.objects.create(name="Old Name")
    activity.name = "New Name"
    activity.save()
    updated_activity = ShopActivity.objects.get(id=activity.id)
    assert updated_activity.name == "New Name"

@pytest.mark.django_db
def test_toggle_is_active():
    activity = ShopActivity.objects.create(name="Toggle Activity")
    activity.is_active = False
    activity.save()
    updated_activity = ShopActivity.objects.get(id=activity.id)
    assert updated_activity.is_active is False

@pytest.mark.django_db
def test_delete_shop_activity():
    activity = ShopActivity.objects.create(name="To be deleted")
    activity_id = activity.id
    activity.delete()
    with pytest.raises(ShopActivity.DoesNotExist):
        ShopActivity.objects.get(id=activity_id)

@pytest.mark.django_db
def test_filter_active_shop_activities():
    active_activity = ShopActivity.objects.create(name="Active Activity", is_active=True)
    inactive_activity = ShopActivity.objects.create(name="Inactive Activity", is_active=False)
    active_activities = ShopActivity.objects.filter(is_active=True)
    assert active_activity in active_activities
    assert inactive_activity not in active_activities
