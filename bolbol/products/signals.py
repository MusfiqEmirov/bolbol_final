from django.db import transaction
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from utils.helpers import shrink_text, generate_slug
from .documents import ProductDocument

from .models import Product, ReactivationRequest, ProductUpdateRequest
from products.tasks import(
    send_product_created_email_task,
    send_product_update_request_email_task,
    send_reactivation_request_email_task,
    send_product_approved_email_task,
    send_product_rejected_email_task
)


@receiver(post_save, sender=Product)
def set_product_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        slug = f"{instance.pk}-{generate_slug(instance.name)}"
        Product.objects.filter(pk=instance.pk).update(slug=slug)


# Elasticsearch signals
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
@receiver(post_save, sender=ProductUpdateRequest)
@receiver(post_save, sender=Product)
def send_created_product_email(sender, instance, created, **kwargs):
    if created:
        def _send_email():
            product = Product.objects.get(pk=instance.pk)
            send_product_created_email_task.delay(product.owner.email, product.slug)
        transaction.on_commit(_send_email)


@receiver(post_save, sender=ProductUpdateRequest)
def send_update_request_email(sender, instance, created, **kwargs):
    if created:
        def _send_email():
            send_product_update_request_email_task.delay(instance.product.owner.email, instance.product.slug)
        transaction.on_commit(_send_email)


@receiver(post_save, sender=ReactivationRequest)
def send_reactivation_email_signal(sender, instance, created, **kwargs):
    if created:
        def _send_email():
            user_email = instance.user.email
            product_slug = instance.product.slug
            send_reactivation_request_email_task.delay(user_email, product_slug)
        
        transaction.on_commit(_send_email)


@receiver(pre_save, sender=Product)
def check_status_change_on_product(sender, instance, **kwargs):
    user_email = instance.owner.email
    product_slug = instance.slug

    if not instance.id:
        return
    try:
        previous = Product.objects.get(id=instance.id)
    except Product.DoesNotExist:
        return

    if previous.status != instance.status:
        if instance.status == Product.APPROVED:
            instance.is_active = True 
            send_product_approved_email_task.delay(user_email, product_slug)

        elif instance.status == Product.REJECTED:
            instance.is_active = False
            send_product_rejected_email_task.delay(user_email, product_slug)


