class ProductSectionConfig:
    HOME_PAGE_VIP_SECTION_PRODUCT_COUNT = 16
    VIP_SECTION_PRODUCT_BUTTON_LINK = '/vip-products/'
    SIMILAR_PRODUCTS_OFFSET = 12


class ProductConfig:
    PRODUCT_MAX_PRICE = 1_000_000_000
    PRODUCT_MIN_PRICE = 0


# class OTPConfig:
#     OTP_EXPIRY = 120             # OTP expiration time in seconds (2 minutes)
#     OTP_COOLDOWN = 60            # Cooldown time for sending OTP in seconds (1 minute)
#     OTP_ATTEMPT_LIMIT = 3        # Maximum number of OTP attempts
#     ATTEMPT_RESET_TIME = 86400   # Reset attempts after 24 hours (in seconds)
#     OTP_LEN = 4

class OTPConfig:
    OTP_EXPIRY = 1000             # OTP expiration time in seconds (2 minutes)
    OTP_COOLDOWN = 60            # Cooldown time for sending OTP in seconds (1 minute)
    OTP_ATTEMPT_LIMIT = 300        # Maximum number of OTP attempts
    ATTEMPT_RESET_TIME = 86400   # Reset attempts after 24 hours (in seconds)
    OTP_LEN = 4


class ComplaintConfig:
    COMPLAINT_BODY_TEXT_SYM_LIMIT = 3000