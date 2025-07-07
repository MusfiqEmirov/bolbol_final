from django.urls import path
from .views import *


app_name = "apis"

urlpatterns = [
    # Product endpoints
    path(
        'products/delete-multiple/',
        MultiDeleteProductView.as_view(), 
        name='bulk-delete-products'
    ),
    path(
        "search/",
        ProductSearchAPIView.as_view(),
        name="product-search"
    ),
    path(
        "product-cards/",
        ProductCardListAPIView.as_view(),
        name="product-cards"
    ),
    path(
        "products/",
        ProductCreateAPIView.as_view(),
        name="product-create"
    ),
    path(
        "products/<slug:product_slug>/",
        ProductDetailAPIView.as_view(),
        name="product-detail"
    ),
    path(
        "similar-products/<slug:product_slug>/",
        SimilarProductListAPIView.as_view(),
        name="similar-product-list"
    ),

    path(
        "transport-products/",
        TransportProductFilterAPIView.as_view(),
        name="transport-product-filter"
    ),
    path(
        "real-estate/",
        RealEstateProductFilterAPIView.as_view(),
        name="real-estate-product-filter"
    ),
    # City endpoints
    path(
        "cities/",
        CityListAPIView.as_view(),
        name="cities"
    ),

    # Category endpoints
    path(
        "categories/",
        CategoryAPIView.as_view(),
        name="categories"
    ),

    # Auth endpoints
    path(
        "auth/login/send-otp/",
        SendOTPAPIView.as_view(),
        name="send-otp"
    ),
    path(
        "auth/login/verify-otp/",
        VerifyOTPAPIView.as_view(),
        name="verify-otp"
    ),

    # JWT urls
    path(
        "token/", 
        TokenObtainPairView.as_view(),
        name="token-obtain-pair"
    ),
    path(
        "token/refresh/", 
        TokenRefreshView.as_view(), 
        name="token-refresh"
    ),

    # User endpoints
    path(
        "users/<int:pk>/",
        UserDetailAPIView.as_view(), 
        name="user-detail"
    ),

    # Bookmark endpoints
    path(
        "users/bookmarks/", 
        BookmarkAPIView.as_view(), 
        name="bookmark"
    ),

    # Shop endpoints
    path(
        "shops/",
        ShopListAPIView.as_view(),
        name="shop-list"
    ),
    path(
        "shop-activities/",
        ShopActivityListAPIView.as_view(), 
        name="shop-activity-list"
    ),
    path(
        "shop-registration-requests/",
        ShopRegistrationRequestAPIView.as_view(),
        name="shop-registration-request"
    ),

    # Partner Companies endpoint
    path(
        "partner-companies/",
        PartnerCompanyListAPIView.as_view(),
        name="partner-companies",
    ),

    # Comments endpoint
    path(
        "comments/", 
        CommentAPIView.as_view(), 
        name="comment-create"
    ),

    # Complaints endpoint
    path(
        "complaint-categories/", 
        ComplaintCategoryAPIView.as_view(), 
        name="complaint-category-list"
    ),
    path(
        "complaints/", 
        ComplaintCreateAPIView.as_view(), 
        name="complaint-create"
    )
]

category_related_urlpatterns = [
    path(
        "categories/<int:category_pk>/subcategories/",
        SubcategoryAPIView.as_view(),
        name="subcategory-list"
    ),
    path(
        "filter-schemas/<int:category_pk>/<int:subcategory_pk>/",
        SubcategoryFilterSchemaAPIView.as_view(),
        name="subcategory-filter-schema"
    )
]

urlpatterns += category_related_urlpatterns

urlpatterns += [
    path(
        "users/me/",
        UserUpdateAPIView.as_view(),
        name="user-update"
    ),
    path(
        "shops/me/",
        ShopUpdateAPIView.as_view(),
        name="shop-update"
    ),
]