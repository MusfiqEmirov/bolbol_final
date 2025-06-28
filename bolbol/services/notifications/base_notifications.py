import hashlib
import requests

from django.utils.http import urlencode
from django.conf import settings
from celery import shared_task
from utils.helpers import normalize_phone_number

__all__ = ("send_sms_alert",)


@shared_task
def send_sms_alert(phone_number: str, message: str, unicode: bool = None) -> dict:
    """Send an SMS alert to the user."""
    sms_url = settings.SMS_URL
    sms_login = settings.SMS_LOGIN
    sms_sender = settings.SMS_SENDER
    use_unicode = str(settings.SMS_UNICODE).lower()
    sms_password_hashed = hashlib.md5(settings.SMS_PASSWORD.encode()).hexdigest()
    hash_input = f"{sms_password_hashed}{sms_login}{message}{phone_number}{sms_sender}"
    security_key = hashlib.md5(hash_input.encode()).hexdigest()

    params = {
        "login": sms_login,
        "msisdn": phone_number,
        "text": message,
        "sender": sms_sender,
        "key": security_key,
        "unicode": use_unicode,
    }

    request_url = sms_url + urlencode(params)
    response = requests.get(request_url, timeout=10)

    return response.json()

    # try:
    #     request_url = f"{sms_url}?{urlencode(params)}"
    #     response = requests.get(request_url, timeout=10)  # Timeout for reliability
    #     response.raise_for_status()  # Raise exception for HTTP errors
    #     return response.json()
    # except requests.RequestException as e:
    #     # Handle request exceptions
    #     return {"error": str(e), "status_code": response.status_code if 'response' in locals() else None}
    # except ValueError:
    #     # Handle JSON decoding errors
    #     return {"error": "Invalid response format", "status_code": response.status_code if 'response' in locals() else None}