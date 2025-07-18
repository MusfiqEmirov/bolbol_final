from django.urls import path
from .views import *



app_name = "apis"

urlpatterns = [
    # Product endpoints
    path(
        'products/delete-multiple/',
        BulkDeleteProductsAPIView.as_view(), 
        name='bulk-delete-products'
    ),
    path(
        "products/search/",
        ProductsSearchAPIView.as_view(),
        name="products-search"
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
        "products/reactivation/<slug:product_slug>/",
        RequestProductReactivationAPIView.as_view(),
        name="reactivation-product"
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
        "users/products/expired_at/",
        ProductsExpireAtListByUserAPIView.as_view(),
        name = "user-expire-at-products"
    ),
    path(
        "users/products/approved/",
        ProductApprovedListByUserAPIView.as_view(),
        name="user-approved-products"
    ),
    path(
        "users/products/pending/",
        ProductPendingListByUserAPIView.as_view(),
        name="user-pending-products"
    ),
    path(
        "users/<int:pk>/",
        UserDetailAPIView.as_view(), 
        name="user-detail"
    ),
    # path(
    #     "product-cards/mine/",
    #     ProductCardListByUserAPIView.as_view(),
    #     name="user-product-cards"
    # ),
    path(
        "products/mine/<slug:product_slug>/",
        ProductDetailByUserAPIView.as_view(),
        name="user-product-detail"
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
        "shops/shop_id",
        ShopDetailAPIView.as_view(),
        name="shop-profile"
    ),
    path(
        "shops/<int:shop_id>/product-cards/",
        ProductCardListByShopAPIView.as_view(),
        name="shop-product-cards"
    ),
    path(
        "shops/contacts/",
        CreateShopContactAPIView.as_view(),
        name="create-shop-contacts"
    ),
    path(
        "shops/working-hours/",
        ShopWorkingHoursAPIView.as_view(),
        name="create-working-hours"
    ),
    path(
        "shops/<int:contact_id>/contacts/",
        ShopContactsAPIView.as_view(),
        name="shop-contacts"
    ),
    path(
        "shops/<int:working_hours_id>/working-hours/",
        ShopWorkingHoursAPIView.as_view(),
        name="shop-working-hours"
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
    path(
        "shops/search/",
        ShopsSearchAPIView.as_view(),
        name="shops-search"
    ),
    path(
        "shops/filter/",
        ShopFilterAPIView.as_view(),
        name="shops-filter"
    ),

    # Partner Companies endpoint
    path(
        "partner-companies/",
        PartnerCompanyListAPIView.as_view(),
        name="partner-companies",
    ),

    # Comments endpoint
    path(
        "products/<slug:product_slug>/comments/", 
        CommentsByProductAPIView.as_view(), 
        name="product-comments"
    ),
    path(
        "products/<slug:product_slug>/comments/create/", 
        CommentCreateAPIView.as_view(), 
        name="comment-create"
    ),
    path(
        "comments/comment_id", 
        CommentDeleteAPIView.as_view(), 
        name="delete-comment"
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