import pytest
from rest_framework.test import APIClient
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestOTPAPI:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.send_otp_url = reverse("apis:send-otp")
        self.verify_otp_url = reverse("apis:verify-otp")
        self.phone_number = "+994501234567"
        self.normalized_phone = "+994501234567"

    def test_send_otp_missing_phone(self):
        response = self.client.post(self.send_otp_url, data={})
        assert response.status_code == 400
        assert "error" in response.data

    def test_send_otp_invalid_phone(self):
        response = self.client.post(self.send_otp_url, data={"phone_number": "invalid"})
        assert response.status_code == 400
        assert "error" in response.data

    @patch("django.core.cache.cache.get")
    def test_send_otp_rate_limit(self, mock_cache_get):
        mock_cache_get.side_effect = lambda key: True if "otp_cooldown" in key else 0
        response = self.client.post(self.send_otp_url, data={"phone_number": self.phone_number})
        assert response.status_code == 429
        assert "error" in response.data

    def test_verify_otp_missing_fields(self):
        response = self.client.post(self.verify_otp_url, data={"phone_number": self.phone_number})
        assert response.status_code == 400
        assert "error" in response.data

    @patch("django.core.cache.cache.get", return_value=None)
    def test_verify_otp_expired(self, mock_cache_get):
        response = self.client.post(self.verify_otp_url, data={"phone_number": self.phone_number, "otp_code": "123456"})
        assert response.status_code == 400
        assert "error" in response.data

    @patch("django.core.cache.cache.get", return_value="654321")
    def test_verify_otp_invalid_code(self, mock_cache_get):
        response = self.client.post(self.verify_otp_url, data={"phone_number": self.phone_number, "otp_code": "123456"})
        assert response.status_code == 400
        assert "error" in response.data

    @patch("django.core.cache.cache.get", return_value="123456")
    @patch("django.contrib.auth.get_user_model")
    def test_verify_otp_success(self, mock_get_user_model, mock_cache_get):
        user = User(phone_number=self.phone_number)
        user.pk = 1
        mock_get_user_model.return_value.objects.get_or_create.return_value = (user, True)

        response = self.client.post(self.verify_otp_url, data={"phone_number": self.phone_number, "otp_code": "123456"})
        assert response.status_code == 200
        assert response.data["detail"] == "OTP verified successfully!"
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user_id"] == 1
