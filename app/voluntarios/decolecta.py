"""
Cliente de Decolecta (RENIEC) con dos protecciones para el límite de la API:

  1. Deduplicación en tabla (ConsultaReniec): si el DNI ya se consultó hace
     poco, no se vuelve a pedir.
  2. Limitador de caudal (LimitadorApi): cubeta de fichas compartida por
     todos los workers. Nunca salen más consultas por segundo de las que
     permite el plan contratado.

Si hay más demanda de la que la cubeta permite, el request espera hasta
ESPERA_MAXIMA_FICHA segundos y devuelve 503 con un mensaje claro, en vez de
reventar la cuota.
"""
import logging
import re
import time
from datetime import timedelta

import requests
from django.db import transaction
from django.utils import timezone

from .config import (
    API_KEY_DELCO,
    DECOLECTA_CACHE_HORAS,
    DECOLECTA_URL,
    ESPERA_MAXIMA_FICHA,
)
from .models import ConsultaReniec, LimitadorApi

logger = logging.getLogger(__name__)

TIMEOUT = 10
CLAVE_LIMITADOR = "decolecta"
PAUSA = 0.25
INTENTOS = max(1, int(ESPERA_MAXIMA_FICHA / PAUSA))


class ErrorDni(Exception):
    """Error controlado que el controller traduce a una respuesta HTTP."""

    def __init__(self, mensaje, status=400):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.status = status


def _tomar_ficha() -> bool:
    """
    Intenta tomar una ficha. Devuelve True si lo consigue.

    select_for_update() bloquea la fila mientras se recalcula, así que dos
    workers no pueden tomar la misma ficha. El bloqueo dura microsegundos.
    """
    with transaction.atomic():
        try:
            cubeta = LimitadorApi.objects.select_for_update().get(clave=CLAVE_LIMITADOR)
        except LimitadorApi.DoesNotExist:
            logger.warning("Falta la fila '%s' en LimitadorApi", CLAVE_LIMITADOR)
            return True

        ahora = timezone.now()
        transcurrido = max(0.0, (ahora - cubeta.actualizado).total_seconds())

        cubeta.tokens = min(cubeta.capacidad, cubeta.tokens + transcurrido * cubeta.tasa)
        cubeta.actualizado = ahora

        concedida = cubeta.tokens >= 1
        if concedida:
            cubeta.tokens -= 1

        cubeta.save(update_fields=["tokens", "actualizado"])
        return concedida


def _esperar_ficha():
    """
    Espera hasta ESPERA_MAXIMA_FICHA por una ficha.

    Dentro de una transacción externa (ATOMIC_REQUESTS o un atomic del
    llamador) reintentar es contraproducente: el candado de la fila no se
    libera hasta el commit, así que esperar solo bloquea a los demás.
    Medido: 1.7 s de espera para el segundo worker. En ese caso se hace un
    único intento. `manage.py check` avisa de esa configuración (E001).
    """
    from django.db import connection

    if connection.in_atomic_block:
        if _tomar_ficha():
            return
        raise ErrorDni(
            "Hay muchas personas registrándose ahora mismo. "
            "Espera unos segundos y vuelve a intentarlo.",
            503,
        )

    for _ in range(INTENTOS):
        if _tomar_ficha():
            return
        time.sleep(PAUSA)

    logger.warning("Limitador saturado: sin ficha en %ss", ESPERA_MAXIMA_FICHA)
    raise ErrorDni(
        "Hay muchas personas registrándose ahora mismo. "
        "Espera unos segundos y vuelve a intentarlo.",
        503,
    )


def _desde_cache(dni: str):
    limite = timezone.now() - timedelta(hours=DECOLECTA_CACHE_HORAS)
    fila = ConsultaReniec.objects.filter(dni=dni, updated_at__gte=limite).first()
    return fila.como_dict() if fila else None


def _guardar_en_cache(datos: dict):
    ConsultaReniec.objects.update_or_create(
        dni=datos["dni"],
        defaults={
            "nombres": datos["nombres"],
            "apellido_paterno": datos["apellido_paterno"],
            "apellido_materno": datos["apellido_materno"],
            "nombre_completo": datos["nombre_completo"],
        },
    )


def consultar_dni(dni: str) -> dict:
    if not re.fullmatch(r"\d{8}", dni or ""):
        raise ErrorDni("El DNI debe tener 8 dígitos.", 422)

    guardado = _desde_cache(dni)
    if guardado:
        return guardado

    if not API_KEY_DELCO:
        logger.error("API_KEY_DELCO no está configurada")
        raise ErrorDni("El servicio de verificación no está configurado.", 503)

    # A partir de aquí sí se gasta una consulta: pedimos ficha.
    _esperar_ficha()

    try:
        respuesta = requests.get(
            DECOLECTA_URL,
            params={"numero": dni},
            headers={
                "Authorization": f"Bearer {API_KEY_DELCO}",
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT,
        )
    except requests.Timeout:
        raise ErrorDni("RENIEC tardó demasiado en responder. Inténtalo de nuevo.", 504)
    except requests.RequestException:
        logger.exception("Fallo de red al consultar Decolecta")
        raise ErrorDni("No pudimos conectarnos con RENIEC. Inténtalo en un momento.", 503)

    if respuesta.status_code in (400, 404, 422):
        raise ErrorDni("No encontramos ese DNI en RENIEC. Revisa el número.", 404)
    if respuesta.status_code in (401, 403):
        logger.error("Decolecta rechazó el token (%s)", respuesta.status_code)
        raise ErrorDni("El servicio de verificación no está disponible.", 503)
    if respuesta.status_code == 429:
        logger.error("Decolecta devolvió 429: revisar la tasa del limitador")
        raise ErrorDni("Demasiadas consultas. Espera un momento e inténtalo de nuevo.", 429)
    if respuesta.status_code >= 400:
        logger.error("Decolecta respondió %s", respuesta.status_code)
        raise ErrorDni("RENIEC no respondió correctamente. Inténtalo en un momento.", 503)

    try:
        crudo = respuesta.json()
    except ValueError:
        raise ErrorDni("RENIEC devolvió una respuesta inesperada.", 503)

    nombres = (crudo.get("first_name") or "").strip()
    ap_paterno = (crudo.get("first_last_name") or "").strip()
    ap_materno = (crudo.get("second_last_name") or "").strip()

    if not nombres and not ap_paterno:
        raise ErrorDni("No encontramos ese DNI en RENIEC. Revisa el número.", 404)

    completo = (crudo.get("full_name") or f"{ap_paterno} {ap_materno} {nombres}").strip()

    datos = {
        "dni": crudo.get("document_number") or dni,
        "nombres": nombres,
        "apellido_paterno": ap_paterno,
        "apellido_materno": ap_materno,
        "nombre_completo": re.sub(r"\s+", " ", completo),
    }

    _guardar_en_cache(datos)
    return datos
