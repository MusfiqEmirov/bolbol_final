from celery import shared_task
from django.utils import timezone

from products.models import Product
from utils.send_email import send_mail_func


@shared_task
def send_product_created_email_task(user_email, product_slug):
    subject = 'Elanınız moderasiyaya göndərildi'
    message = f"Salam, sizin '{product_slug}' elanınız moderasiyaya göndərildi və ən qısa zamanda baxılacaq."
    send_mail_func(user_email, subject, message)


@shared_task
def send_product_update_request_email_task(user_email, product_slug):
    subject = 'Elanınız üçün dəyişiklik sorğusu alındı'
    message = f"Salam, sizin '{product_slug}' elanınız üçün dəyişiklik sorğusu qəbul edildi. Tezliklə moderasiya olunacaq."
    send_mail_func(user_email, subject, message)


@shared_task
def send_reactivation_request_email_task(user_email, product_slug):
    subject = "Elanı aktivləşdirmə istəyi göndərildi"
    message = f"Sizin '{product_slug}' elanınız üçün aktivləşdirmə istəyi qəbul edildi. Qısa zamanda yoxlanacaq."
    send_mail_func(user_email, subject, message)


@shared_task
def send_product_approved_email_task(user_email, product_slug):
    subject = 'Elanınız təsdiqləndi'
    message = f"Salam, '{product_slug}' elanınız moderasiyadan keçdi və təsdiqləndi."
    send_mail_func(user_email, subject, message)


@shared_task
def send_product_rejected_email_task(user_email, product_slug):
    subject = 'Elanınız rədd edildi'
    message = f"Salam, '{product_slug}' elanınız moderasiyadan keçmədi və rədd edildi."
    send_mail_func(user_email, subject, message)


# Celery beat for deactivate exipred products
@shared_task
def deactivate_expired_products_and_send_email_task():
    now = timezone.now()
    expired_products = Product.objects.filter(expires_at__lte=now, is_active=True)
    for product in expired_products:
        product.deactivate()
        subject = 'Elan müddəti başa çatdı'
        message = f"Sizin '{product.slug}' elanınızın müddəti başa çatdığı üçün deaktiv edildi."
        send_mail_func(product.owner.email, subject, message)


