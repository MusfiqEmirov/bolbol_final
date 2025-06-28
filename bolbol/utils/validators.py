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