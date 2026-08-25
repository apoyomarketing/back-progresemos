"""Lógica de negocio del registro de voluntarios."""
import logging
import re

from django.db import IntegrityError, transaction

from . import decolecta
from .decolecta import ErrorDni
from .models import Voluntario

logger = logging.getLogger(__name__)


class YaRegistrado(Exception):
    """El DNI ya tiene una preinscripción."""

    def __init__(self, codigo):
        super().__init__("Este DNI ya está preinscrito.")
        self.codigo = codigo


def _limpiar(valor):
    return str(valor or "").strip()


def validar_formato_dni(dni):
    dni = _limpiar(dni)
    if not re.fullmatch(r"\d{8}", dni):
        raise ErrorDni("El DNI debe tener 8 dígitos.", 422)
    return dni


def validar_formato_celular(celular):
    celular = _limpiar(celular)
    if not re.fullmatch(r"9\d{8}", celular):
        raise ErrorDni("El celular debe tener 9 dígitos y empezar con 9.", 422)
    return celular


def obtener_ip(request):
    """Detrás de Traefik/Coolify la IP real viene en X-Forwarded-For."""
    reenviada = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if reenviada:
        return reenviada.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def consultar_persona(dni):
    """
    Paso 2 del modal: devuelve los datos de RENIEC.

    Comprueba el duplicado ANTES de consultar para no gastar un crédito en
    alguien que ya está registrado.
    """
    dni = validar_formato_dni(dni)

    existente = Voluntario.objects.filter(dni=dni).only("codigo").first()
    if existente:
        raise YaRegistrado(existente.codigo)

    return decolecta.consultar_dni(dni)


def registrar(dni, celular, acepta_whatsapp, request):
    """
    Paso 3 del modal: crea la preinscripción.

    El nombre NUNCA viene del navegador: se vuelve a pedir a RENIEC (casi
    siempre desde la caché, así que no cuesta otro crédito).
    """
    dni = validar_formato_dni(dni)
    celular = validar_formato_celular(celular)

    if not acepta_whatsapp:
        raise ErrorDni(
            "Necesitamos tu autorización para escribirte por WhatsApp.", 422
        )

    existente = Voluntario.objects.filter(dni=dni).only("codigo").first()
    if existente:
        raise YaRegistrado(existente.codigo)

    persona = decolecta.consultar_dni(dni)

    try:
        # atomic() abre un savepoint: si el INSERT choca con el dni único,
        # se revierte solo ese punto y la conexión sigue usable.
        #
        # Se guarda `dni` (el validado de la petición), NO persona["dni"].
        # Son el mismo número, pero si alguna vez difirieran, la fila se
        # insertaría con uno y la comprobación de duplicado buscaría el otro:
        # el 409 se convertiría en un 500 y el usuario quedaría sin registro.
        with transaction.atomic():
            return Voluntario.objects.create(
                dni=dni,
                nombres=persona["nombres"],
                apellido_paterno=persona["apellido_paterno"],
                apellido_materno=persona["apellido_materno"],
                nombre_completo=persona["nombre_completo"],
                celular=celular,
                acepta_whatsapp=True,
                origen="web_unete",
                ip=obtener_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:400],
            )
    except IntegrityError:
        # Puede ser choque de DNI (otra pestaña ganó la carrera) o, con
        # probabilidad ínfima, choque del código generado. Hay que
        # distinguirlos: decirle "ya estás preinscrito" a alguien que no lo
        # está lo dejaría fuera sin remedio.
        duplicado = Voluntario.objects.filter(dni=dni).only("codigo").first()
        if duplicado:
            raise YaRegistrado(duplicado.codigo)
        logger.exception("IntegrityError sin DNI duplicado (¿colisión de código?)")
        raise
