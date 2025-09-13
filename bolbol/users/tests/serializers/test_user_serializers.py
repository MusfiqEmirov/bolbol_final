import pytest
from unittest.mock import PropertyMock, patch
from django.contrib.auth import get_user_model
from model_bakery import baker
from users.serializers import UserSerializer, ProductOwnerMiniProfileSerializer, UserUpdateSerializer

User = get_user_model()

@pytest.mark.django_db
def test_user_serializer_fields_and_values():
    user = baker.make(User, phone_number="994501234567", full_name="Elvin Haxverdiyev", email="elvin@example.com", is_active=True)
    
    # Property-ləri mock edirik:
    with patch.object(User, 'active_products_count', new_callable=PropertyMock) as mock_active_count, \
         patch.object(User, 'product_count_by_category', new_callable=PropertyMock) as mock_cat_count:
        
        mock_active_count.return_value = 5
        mock_cat_count.return_value = {"Electronics": 3, "Books": 2}
        
        serializer = UserSerializer(user)
        data = serializer.data
        
        assert data["phone_number"] == "994501234567"
        assert data["full_name"] == "Elvin Haxverdiyev"
        assert data["email"] == "elvin@example.com"
        assert data["is_active"] is True
        assert data["active_products_count"] == 5
        assert data["product_count_by_category"] == {"Electronics": 3, "Books": 2}

@pytest.mark.django_db
def test_product_owner_mini_profile_serializer():
    user = baker.make(User, phone_number="994509876543", full_name="Test User")
    
    with patch.object(User, 'is_shop_profile', new_callable=PropertyMock) as mock_is_shop, \
         patch.object(User, 'active_products_count', new_callable=PropertyMock) as mock_active_count:
        mock_is_shop.return_value = False
        mock_active_count.return_value = 2
        
        serializer = ProductOwnerMiniProfileSerializer(user)
        data = serializer.data
        
        assert data["phone_number"] == "994509876543"
        assert data["full_name"] == "Test User"
        assert data["is_shop_profile"] is False
        assert data["active_products_count"] == 2

@pytest.mark.django_db
def test_user_update_serializer_valid_data():
    user = baker.make(User, phone_number="994501111111", full_name="Old Name", email="old@example.com")

    update_data = {
        "phone_number": "994502222222",  # Düzgün formatda nömrə
        "full_name": "New Name",
        "email": "new@example.com"
    }

    serializer = UserUpdateSerializer(user, data=update_data)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()

    assert updated_user.phone_number == "994502222222"
    assert updated_user.full_name == "New Name"
    assert updated_user.email == "new@example.com"

@pytest.mark.django_db
def test_user_update_serializer_invalid_phone_number():
    user = baker.make(User, phone_number="994501111111", full_name="Old Name", email="old@example.com")

    update_data = {
        "phone_number": "0502222222",  # Yanlış format
        "full_name": "New Name",
        "email": "new@example.com"
    }

    serializer = UserUpdateSerializer(user, data=update_data)
    assert not serializer.is_valid()
    assert "phone_number" in serializer.errors
