from typing import Optional
from utils.configs import OTPConfig

__all__ = (
    "shrink_text",
    "generate_slug",
    "generate_otp_code",
    "normalize_phone_number",
    "mask_user_fullname"
)


def shrink_text(text, max_length=100) -> str:
    """
    Trims the input text to the specified maximum length and appends an ellipsis ("...") 
    if the text exceeds the maximum length.
    
    Args:
        text (str): The text to be shrunk.
        max_length (int, optional): The maximum length of the text. Defaults to 100.
    
    Returns:
        str: The shrunk text with ellipsis if necessary.
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def generate_slug(text: str) -> str:
    """
    Converts the input text to a URL-friendly slug by converting it to lowercase 
    and replacing spaces with hyphens.
    
    Args:
        text (str): The text to be converted to a slug.
    
    Returns:
        str: The URL-friendly slug.
    """
    return text.lower().replace(" ", "-")


def generate_otp_code(length=OTPConfig.OTP_LEN) -> str:
    """
    Generates a random one-time password (OTP) code consisting of numeric digits 
    with the specified length.
    
    Args:
        length (int, optional): The length of the OTP code. Defaults to OTPConfig.OTP_LEN.
    
    Returns:
        str: The generated OTP code.
    """
    from django.utils.crypto import get_random_string
    otp_code = get_random_string(length=length, allowed_chars="0123456789")
    return otp_code


def normalize_phone_number(phone_number: str) -> str:
    """
    Removes the leading '+' from the phone number if it exists.
    
    Args:
        phone_number (str): The phone number to normalize.

    Returns:
        str: The normalized phone number.
    """
    return phone_number.lstrip("+")


def mask_user_fullname(full_name: Optional[str]) -> str:
    """
    Masks each part of the author's full name for privacy.
    - Example:
        - "John" -> "J***"
        - "John Doe" -> "J*** D***"
        - "John Michael Doe" -> "J*** M*** D***"
    """
    if not full_name:
        return "Anonymous"

    words = full_name.split()
    masked_words = [f"{word[0]}***" for word in words]
    return " ".join(masked_words)
