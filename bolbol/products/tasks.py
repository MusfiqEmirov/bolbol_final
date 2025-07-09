from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_product_created_email_task(user_email, product_slug):
    subject = 'Elan uğurla yaradıldı'
    message = f"Salam, sizin '{product_slug}' elanınız uğurla yaradıldı."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
