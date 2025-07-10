from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import re
from django.core.exceptions import ValidationError


AZERBAIJANI_PHONE_PATTERN = r"^994\d{9}$"

def validate_phone_number(value: str, pattern: str = AZERBAIJANI_PHONE_PATTERN) -> None:
    """
    Validates that the phone number matches the Azerbaijani format: 994XXXXXXXXX.

    Args:
        value (str): The phone number to validate.
        pattern (str, optional): The regex pattern to match the phone number. 
        Defaults to Azerbaijani format: 994XXXXXXXXX.

    Raises:
        ValidationError: If the phone number does not match the pattern.
    """
    value = value.strip().replace(" ", "").replace("-", "")

    if not re.match(pattern, value):
        raise ValidationError(
            f"Invalid phone number: {value}. It must be in the format 994XXXXXXXXX."
        )


az_slug_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9əöşçğıüƏÖŞÇĞİÜ_-]+$',
    message='Enter a valid “slug” consisting of letters, numbers, underscores, hyphens or Azerbaijani characters.'
)


def max_30_days_validator(value):
    now = timezone.now()
    if value - now > timedelta(days=30):
        raise ValidationError("Elanın bitmə tarixi 30 gündən çox ola bilməz.")
    
    
def min_7_days_validator(value):
    now = timezone.now()
    if value - now < timedelta(days=7):
        raise ValidationError("Elanın bitmə tarixi ən azı 7 gün sonra olmalıdır.")