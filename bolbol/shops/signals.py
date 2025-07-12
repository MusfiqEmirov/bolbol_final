from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from shops.models import Shop
from shops.documents import ShopDocument


# Elasticsearch signals
@receiver(post_save, sender=Shop)
def update_product_document(sender, instance, **kwargs):
    ShopDocument().update(instance)


@receiver(post_delete, sender=Shop)
def delete_product_document(sender, instance, **kwargs):
    try:
        ShopDocument().get(id=instance.id).delete()
    except Exception:
        pass