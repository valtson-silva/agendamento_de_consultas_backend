from celery import shared_task
from .emails import send_email_reminder

# Task para automatizar o envio de emails
@shared_task
def rent_reminder():
    send_email_reminder()
