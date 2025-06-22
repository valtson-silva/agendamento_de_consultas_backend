from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q
from decouple import config

from .models import Queries


def send_email_reminder():
    """Envia emails para os pacientes com consultas próximas"""
    
    close_consultation = now() + timedelta(days=2)
    
    queries = Queries.objects.filter(
        Q(status="agendada") & Q(date_hour__lte=close_consultation)
    )
    
    for query in queries:
        patient_email = query.patient.email
        date = query.date_hour.strftime("%d/%m/%Y %H:%M")
        message = f"Olá {query.patient.name}, sua consulta está agendada para {date}. Por favor não se esqueça e esteja pronto!"
        
        send_mail(
            "Lembrete da consulta",
            message,
            config("EMAIL_HOST_USER"),
            [patient_email],
            fail_silently=False
        )
        