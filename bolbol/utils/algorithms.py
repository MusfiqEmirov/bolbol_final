from django.db.models import Q, F, Value, IntegerField, Case, When
from utils.configs import ProductSectionConfig as PSConfig
from products.models import Product


def _get_similar_products(main_product: Product, 
                          limit: int = PSConfig.SIMILAR_PRODUCTS_OFFSET):
    """
    Get similar products based on category, city, and shared attributes.
    Uses weighted similarity scoring to rank results by relevance.
    """
    similar_products = Product.objects.filter(is_active=True,
                                              category=main_product.category
                                            ).exclude(
                                                pk=main_product.pk
                                            )
    # similarity_cases = Case(
    #     # 80% Similarity - Same category & same city
    #     When(Q(category=main_product.category) & Q(city=main_product.city), then=Value(80)),

    #     # 60% Similarity - Same category only
    #     When(Q(category=main_product.category), then=Value(60)),

    #     # 40% Similarity - Same city only
    #     When(Q(city=main_product.city), then=Value(40)),

    #     # 20% Similarity - Matching other attributes (barter, credit, delivery)
    #     When(
    #         Q(is_barter_available=main_product.is_barter_available) |
    #         Q(is_credit_available=main_product.is_credit_available) |
    #         Q(is_delivery_available=main_product.is_delivery_available),
    #         then=Value(20)
    #     ),
    #     default=Value(0),  # Default similarity score
    #     output_field=IntegerField()
    # )

    # similar_products = Product.objects.filter(
    #     Q(category=main_product.category) | 
    #     Q(city=main_product.city) | 
    #     Q(is_barter_available=main_product.is_barter_available) |
    #     Q(is_credit_available=main_product.is_credit_available) |
    #     Q(is_delivery_available=main_product.is_delivery_available),
    #     is_active=True
    # ).exclude(pk=main_product.pk)

    # # Annotate similarity percentage & order results
    # similar_products = similar_products.annotate(similarity=similarity_cases).order_by(
    #     "-similarity", "-is_super_chance", "-is_premium", "-is_vip", "-updated_at"
    # )

    return similar_products[:limit]