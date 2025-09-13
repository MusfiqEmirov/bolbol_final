from celery import shared_task
from utils.send_email import send_mail_func


@shared_task
def send_shop_registration_request_create_email_task(user_email):
    subject = 'Mağaza qeydiyyatı üçün sorğu göndərildi'
    message = f"Salam, sizin mağaza qeydiyyatı üçün sorğunuz qəbul edildi və nəzərdən keçiriləcək."
    send_mail_func(user_email, subject, message)


@shared_task
def send_shop_registration_request_approved_email_task(user_email):
    subject = 'Mağaza qeydiyyatınız uğurla təsdiqləndi'
    message = f"Salam, mağaza qeydiyyatınız uğurla təsdiqləndi."
    send_mail_func(user_email, subject, message)


@shared_task
def send_shop_registration_request_rejected_email_task(user_email):
    subject = 'Mağaza qeydiyyatınız rədd edildi'
    message = f"Salam, elanınız moderasiyadan keçmədi və rədd edildi."
    send_mail_func(user_email, subject, message)


# @shared_task
# def send_shop_update_request_email_task(user_email):
#     subject = 'Mağazanız üçün dəyişiklik sorğusu alındı'
#     message = f"Salam, sizin mağazanız üçün dəyişiklik sorğusu qəbul edildi. Tezliklə moderasiya olunacaq."
#     send_mail_func(user_email, subject, message)