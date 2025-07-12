from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl import Q

from products.documents import ProductDocument
from utils.paginations import ProductPagination 


__all__ = [
    "ProductsSearchAPIView"
]

class ProductsSearchAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get(self, request):
        query = request.GET.get("query", "").strip()

        if not query:
            return Response({"error": "Query param is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            q = Q("term", is_active=True) & (
                Q("match", name={"query": query, "fuzziness": "auto"}) |
                Q("prefix", name=query) |
                Q("match_phrase_prefix", name=query)
            )
            search = ProductDocument.search().query(q)
            response = search.execute()
            results = [{"id": hit.id, "name": hit.name} for hit in response]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Elasticsearch error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )