from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction

from shops.models import Shop, ShopRegistrationRequest
from shops.documents import ShopDocument
from shops.tasks import (
    send_shop_registration_request_create_email_task,
    send_shop_registration_request_approved_email_task,
    send_shop_registration_request_rejected_email_task,
)


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


# Email signals
@receiver(post_save, sender=ShopRegistrationRequest)
def send_shop_registration_request(sender, instance, created, **kwargs):
    if created:
        def _send_email():
            user_email = instance.shop_owner.email
            send_shop_registration_request_create_email_task.delay(user_email)
        transaction.on_commit(_send_email)


@receiver(pre_save, sender=ShopRegistrationRequest)
def check_status_change_on_shop_registration_request(sender, instance, **kwargs):
    user_email = instance.shop_owner.email

    if not instance.id:
        return
    try:
        previous = ShopRegistrationRequest.objects.get(id=instance.id)
    except ShopRegistrationRequest.DoesNotExist:
        return

    if previous.status != instance.status:
        if instance.status == ShopRegistrationRequest.APPROVED:
            send_shop_registration_request_approved_email_task.delay(user_email)

        elif instance.status == ShopRegistrationRequest.REJECTED:
            send_shop_registration_request_rejected_email_task.delay(user_email)
