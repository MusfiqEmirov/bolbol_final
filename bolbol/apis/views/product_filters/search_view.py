from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl import Q

from products.documents import ProductDocument
from utils.paginations import ProductPagination 

__all__ = [
    "ProductSearchAPIView"
]

class ProductSearchAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    pagination_class = ProductPagination

    def get(self, request):
        query = request.GET.get("query", "").strip()
        if not query:
            return Response({"error": "Query param is required"}, status=status.HTTP_400_BAD_REQUEST)

        q = Q("bool", must=[
            Q("term", is_active=True),
            Q(
                "bool",
                should=[
                    Q("match", name={"query": query, "fuzziness": "auto"}),
                    Q("prefix", name=query),
                    Q("match_phrase_prefix", name=query),
                ],
                minimum_should_match=1,
            ),
        ])

        search = ProductDocument.search().query(q)
        response = search.execute()

        results = [{"id": hit.id, "name": hit.name} for hit in response]
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(results, request, view=self)

        return paginator.get_paginated_response(page or [])