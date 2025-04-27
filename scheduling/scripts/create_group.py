import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointment_scheduling.settings')  
django.setup()

from django.contrib.auth.models import Group, Permission

def create_group():
    if not Group.objects.filter(name="Professionals").exists():
        group = Group.objects.create(name="Professionals")
        print("Grupo Professionals criado.")
    else:   
        group = Group.objects.get(name="Professionals")
    
    try:
        perm = Permission.objects.get(codename="permission_for_professionals")
        group.permissions.add(perm)
        print("Permissão permission_for_professionals adicionada ao grupo Professionals.")
    except Permission.DoesNotExist:
        print("Permissão permission_for_professionals não encontrada. Verifique se você já fez as migrations.")
        

if __name__ == "__main__":
    create_group()
    