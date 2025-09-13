import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(phone_number="0501234567", password="testpassword123")
    assert user.phone_number == "0501234567"
    assert user.check_password("testpassword123")
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_without_phone_number():
    with pytest.raises(ValueError) as exc:
        User.objects.create_user(phone_number=None, password="testpassword123")
    assert str(exc.value) == "The phone number must be set"


@pytest.mark.django_db
def test_create_superuser_success():
    admin_user = User.objects.create_superuser(phone_number="0507654321", password="adminpassword")
    assert admin_user.phone_number == "0507654321"
    assert admin_user.check_password("adminpassword")
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True
    assert admin_user.is_active is True


@pytest.mark.django_db
def test_create_superuser_with_is_staff_false():
    with pytest.raises(ValueError) as exc:
        User.objects.create_superuser(
            phone_number="0507654321",
            password="adminpassword",
            is_staff=False
        )
    assert str(exc.value) == "Superuser must have is_staff=True."


@pytest.mark.django_db
def test_create_superuser_with_is_superuser_false():
    with pytest.raises(ValueError) as exc:
        User.objects.create_superuser(
            phone_number="0507654321",
            password="adminpassword",
            is_superuser=False
        )
    assert str(exc.value) == "Superuser must have is_superuser=True."
