from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from utils.helpers import shrink_text, generate_slug
from .documents import ProductDocument

from .models import Product
from products.tasks import send_product_created_email_task


@receiver(post_save, sender=Product)
def set_product_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        slug = f"{instance.pk}-{generate_slug(instance.name)}"
        Product.objects.filter(pk=instance.pk).update(slug=slug)


@receiver(post_save, sender=Product)
def update_product_document(sender, instance, **kwargs):
    ProductDocument().update(instance)


@receiver(post_delete, sender=Product)
def delete_product_document(sender, instance, **kwargs):
    try:
        ProductDocument().get(id=instance.id).delete()
    except Exception:
        pass


# Email signals
@receiver(post_save, sender=Product)
def set_product_slug(sender, instance, created, **kwargs):
    user_email = instance.owner.email
    product_slug = instance.slug
    send_product_created_email_task.delay(user_email, product_slug)


