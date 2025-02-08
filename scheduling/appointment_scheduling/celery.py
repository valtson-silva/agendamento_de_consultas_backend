from celery import Celery
import os

# Define as configurações padrão do Django para o Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appointment_scheduling.settings")

app = Celery("appointment_scheduling")

# Carrega as configurações do Celery do settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.update(
    broker_url='redis://redis:6379/0',
    result_backend='redis://redis:6379/0',
    timezone='UTC',
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',
)

# Descobre automaticamente tasks nas APIs registradas
app.autodiscover_tasks()