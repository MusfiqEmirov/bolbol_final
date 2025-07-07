from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from products.models import Product, Comment
from products.serializers import CommentCreateSerializer, CommentSerializer


__all__ = (
    "CommentsByProductAPIView",
    "CommentCreateAPIView",
)


class CommentsByProductAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get(self, request, product_slug, *args, **kwargs):
        try:
            product = Product.objects.get(slug=product_slug)
            comments = Comment.objects.filter(product=product)
            serializer = CommentSerializer(comments,many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=400)



class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, product_slug, *args, **kwargs):
        product = Product.objects.get(slug=product_slug)
        serializer = CommentCreateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)