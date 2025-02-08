from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Queries
from django.db.models import Q
from decouple import config

def send_email_reminder():
    # Envia emails para os pacientes com consultas próximas
    
    close_consultation = now() + timedelta(days=2)
    
    # Obtém as consultas próximas
    queries = Queries.objects.filter(
        Q(status="agendada") & Q(date_hour__lte=close_consultation)
    )
    
    # Itera sobre as consultas próximas
    for query in queries:
        patient_email = query.patient.email
        message = f"Olá {query.patient.name}, sua consulta está agendada para {query.date_hour}. Por favor não se esqueça e esteja pronto!"
        
        # Envia o email
        send_mail(
            "Lembrete da consulta",
            message,
            config("EMAIL_HOST_USER"),
            [patient_email],
            fail_silently=False
        )
        