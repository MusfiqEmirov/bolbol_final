from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from shops.documents import ShopDocument
from elasticsearch_dsl import Q


class ShopFilterAPIView(APIView):
    """
    Filter shops by activity and sort order.

    Supported query parameters:
    - activities: list of activity names (e.g., ?activities=Cleaning&activities=Delivery)
    - sort: one of ['name_asc', 'name_desc', 'product_count_desc', 'random']
    """
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    activities_param = openapi.Parameter(
    'activities',
    openapi.IN_QUERY,
    description="List of activity names (can be multiple, e.g., ?activities=Cleaning&activities=Delivery)",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING),
    collection_format='multi'
    )
    sort_param = openapi.Parameter(
    'sort',
    openapi.IN_QUERY,
    description="Sorting method: name_asc, name_desc, product_count_desc, or random",
    type=openapi.TYPE_STRING,
    enum=['name_asc', 'name_desc', 'product_count_desc', 'random']
    )
    
    @swagger_auto_schema(
        manual_parameters=[activities_param, sort_param],
        operation_summary="Filter and sort shops",
        operation_description="Filter shops by activities and sort order. You can pass multiple activities.",
        responses={
            200: openapi.Response(
                description="List of filtered and sorted shops",
                examples={
                    "application/json": [
                        {"id": 1, "name": "Shop A", "product_count": 12},
                        {"id": 2, "name": "Shop B", "product_count": 8},
                    ]
                }
            )
        }
    )

    def get(self, request):
        sort = request.GET.get("sort")
        activities = request.GET.getlist("activities") 

        search = ShopDocument.search()

        if activities:
            nested_query = Q(
                "nested", 
                path="activities", 
                query=Q("terms", **{"activities.name.keyword": activities}))
            search = search.filter(nested_query)

        if sort == "name_asc":
            search = search.sort('name.raw')
        elif sort == "name_desc":
            search = search.sort('-name.raw')
        elif sort == "product_count_desc":
            search = search.sort('-product_count')
        elif sort == "random":
            search = search.sort({
                "_script": {
                    "type": "number",
                    "script": "Math.random()",
                    "order": "asc"
                }
            })
        else:
            search = search.sort('name.raw') 
        response = search.execute()

        results = []
        for hit in response:
            results.append({
                "id": hit.id,
                "name": hit.name,
                "product_count": hit.product_count,
            })
        return Response(results, status=status.HTTP_200_OK)