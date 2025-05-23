# Generated by Django 5.1.5 on 2025-04-26 21:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('professionals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_hour', models.DateTimeField()),
                ('status', models.CharField(choices=[('agendada', 'Agendada'), ('realizada', 'Realizada'), ('cancelada', 'Cancelada')], max_length=100)),
                ('observations', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patients')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='professionals.professionals')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='professionals.specialty')),
            ],
        ),
    ]
