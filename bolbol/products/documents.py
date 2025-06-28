from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from products.models import Product

product_index = Index('products')  # Elasticsearch index adı

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'is_active',
            'is_vip',
            'is_premium',
            'is_promoted',
            'status',
            'slug'
        ]
