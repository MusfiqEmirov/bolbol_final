from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from shops.models import Shop


product_index = Index('shops')  

@registry.register_document
class ShopDocument(Document):
    name = fields.TextField(
        analyzer="standard",
        fields={
            "raw": fields.KeywordField(),
            "suggest": fields.CompletionField(),  
        }
    )

    activities = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    city = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    product_count = fields.IntegerField(attr='get_product_count')

    class Index:
        name = 'shops'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Shop
        fields = [
            'id',
            'address',
            'bio',
            'map_link',
            'map_latitude',
            'map_longitude',
            'is_active',
            'created_at',
            'updated_at',
        ]