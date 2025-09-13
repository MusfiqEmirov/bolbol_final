from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from products.models import Product, Comment
from products.serializers import CommentCreateSerializer, CommentSerializer


__all__ = (
    "CommentsByProductAPIView",
    "CommentCreateAPIView",
    "CommentDeleteAPIView",
)


class CommentsByProductAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get(self, request, product_slug, *args, **kwargs):
        product = get_object_or_404(Product.objects.filter(is_active=True), slug=product_slug)
        comments = Comment.objects.filter(product=product)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

      
class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, product_slug, *args, **kwargs):
        author = request.user
        product = get_object_or_404(Product.objects.filter(is_active=True), slug=product_slug)
        serializer = CommentCreateSerializer(
            data=request.data, context={
            "author": author,
            "product": product
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["delete"]

    def delete(self, request, comment_id, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(
            Comment.objects.filter(author=user), 
            id=comment_id
        )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)