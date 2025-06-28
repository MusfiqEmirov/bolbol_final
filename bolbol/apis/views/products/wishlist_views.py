from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from products.models import Product, Wishlist
from products.serializers import ProductCardSerializer

__all__ = ("BookmarkAPIView",)


class BookmarkAPIView(APIView):
    """
    API endpoint for bookmarking products (add/remove from wishlist) 
    and retrieving all bookmarked products.
    Requires JWT authentication for identifying the user.
    """
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve all products bookmarked by the authenticated user.
        """
        bookmarks = Wishlist.objects.filter(user=request.user).select_related("product")

        products = [bookmark.product for bookmark in bookmarks]

        serializer = ProductCardSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"error": "Product ID is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, pk=product_id)

        if not request.user or not request.user.is_authenticated:
            return Response(
                {"error": "Authentication is required to bookmark products."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        bookmark = Wishlist.objects.filter(product=product, user=request.user).first()

        if bookmark:
            bookmark.delete()
            return Response(
                {
                    "message": "Product removed from wishlist.",
                    "status": "removed"
                    }, 
                status=status.HTTP_200_OK
            )

        Wishlist.objects.create(product=product, user=request.user)
        return Response(
            {
                "message": "Product added to wishlist.",
                "status": "added"
            }, 
            status=status.HTTP_201_CREATED
        )



        
