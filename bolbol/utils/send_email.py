from django.conf import settings
from django.core.mail import send_mail

__all__ = [
    'send_mail_func'
]

def send_mail_func(user_email, custom_subject, custom_message):
    subject = custom_subject
    message = custom_message
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(
        subject, 
        message, 
        from_email, 
        recipient_list, 
        fail_silently=True
    )
