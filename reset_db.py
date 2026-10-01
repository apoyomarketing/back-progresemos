import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

print("Eliminando tablas antiguas...")
with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS voto CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS mesa CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS tipo_eleccion CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS partido CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS local_votacion CASCADE;")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'escrutinio';")

print("Limpieza completada.")
