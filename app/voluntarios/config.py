"""
Configuración de la app `voluntarios`.

Cada valor se busca en este orden:
    1. Variable de entorno   (lo que pongas en Coolify)
    2. settings.py           (si el proyecto la define)
    3. El valor por defecto de este archivo
"""
import os

from django.conf import settings


def _leer(nombre, defecto):
    valor = os.getenv(nombre)
    if valor:
        return valor
    return getattr(settings, nombre, defecto)


# API key de Decolecta. Se toma de la variable de entorno API_KEY_DELCO
# (en Coolify o en .env local); sin ella, consultar_dni() rechaza con 503.
API_KEY_DELCO = _leer("API_KEY_DELCO", "")

DECOLECTA_URL = _leer("DECOLECTA_URL", "https://api.decolecta.com/v1/reniec/dni")

# Horas que se conserva una consulta antes de volver a pedirla a RENIEC.
DECOLECTA_CACHE_HORAS = int(_leer("DECOLECTA_CACHE_HORAS", "24"))

# Segundos que un request espera una ficha del limitador antes de rendirse.
ESPERA_MAXIMA_FICHA = float(_leer("DECOLECTA_ESPERA_MAXIMA", "3"))

# Desde qué número arranca el correlativo de los códigos (PRG-0001, PRG-0002…).
#
# Con 0, el primer voluntario recibe PRG-0001, y el código revela cuántos
# registros lleva la campaña. Si prefieres que no se note, pon por ejemplo
# 1200 y el primero será PRG-1201.
#
# Solo tiene efecto sobre los registros NUEVOS: los ya emitidos no cambian.
CODIGO_INICIO = int(_leer("VOLUNTARIOS_CODIGO_INICIO", "0"))
