from rest_framework.pagination import PageNumberPagination
from bolbol.utils.configs import ProductSectionConfig


class ProductPagination(PageNumberPagination):
    page_size = ProductSectionConfig.HOME_PAGE_VIP_SECTION_PRODUCT_COUNT