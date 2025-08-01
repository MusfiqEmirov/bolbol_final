from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl import Q

from shops.documents import ShopDocument

__all__ = (
    "ShopsSearchAPIView",
)

class ShopsSearchAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    query_param = openapi.Parameter(
    'query',
    openapi.IN_QUERY,
    description="Search query for shop name",
    type=openapi.TYPE_STRING,
    required=True
    )
    
    @swagger_auto_schema(
    manual_parameters=[query_param],
    operation_summary="Search shops",
    operation_description="Search shops by name using Elasticsearch fuzzy and prefix matching.",
    responses={
        200: openapi.Response(
            description="List of matched shops",
            examples={
                "application/json": [
                    {"id": 1, "name": "Shop A"},
                    {"id": 2, "name": "Shop B"}
                ]
            }
        ),
        400: "Query param is required",
        500: "Elasticsearch error"
    }
    )

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
            search = ShopDocument.search().query(q)
            response = search.execute()

            results = [
                {"id": hit.id, "name": hit.name}
                for hit in response
            ]

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Elasticsearch error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )