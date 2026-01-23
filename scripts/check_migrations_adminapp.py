import os
import sys
sys.path.insert(0, r"C:\CineMatch\Cinematch")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cinematch.settings')
import django
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM django_migrations WHERE app='adminapp' ORDER BY id")
    rows = cursor.fetchall()
print(rows)