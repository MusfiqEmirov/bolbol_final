from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from products.documents import ProductDocument
from utils.paginations import ProductPagination 

__all__ = [
    "ProductSearchAPIView"
]

class ProductSearchAPIView(APIView):
    """Search products using Elasticsearch and return paginated results."""

    permission_classes = [AllowAny]
    http_method_names = ["get"]
    pagination_class = ProductPagination

    def get(self, request):
        query = request.GET.get("query", "").strip()
        if not query:
            return Response({"error": "Query param is required"}, status=status.HTTP_400_BAD_REQUEST)

        search = ProductDocument.search().query("match", name=query)
        response = search.execute()

        results = [{"id": hit.id, "name": hit.name} for hit in response]

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(results, request, view=self)
        return paginator.get_paginated_response(page)
