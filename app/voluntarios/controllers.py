from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from . import services
from .decolecta import ErrorDni


class VoluntariosThrottle(AnonRateThrottle):
    """Límite por IP. La tasa vive en REST_FRAMEWORK.DEFAULT_THROTTLE_RATES."""

    scope = "voluntarios"


def serializar_voluntario(voluntario):
    return {
        "codigo": voluntario.codigo,
        "nombre_completo": voluntario.nombre_completo,
        "estado": voluntario.estado,
    }


@api_view(["POST"])
@authentication_classes([])          # endpoint público: sin JWT, sin sesión, sin CSRF
@permission_classes([AllowAny])      # el proyecto usa IsAuthenticatedOrReadOnly por defecto
@throttle_classes([VoluntariosThrottle])
def validar_dni(request):
    """POST /api/voluntarios/validar-dni/ — paso 2 del modal."""
    try:
        persona = services.consultar_persona(request.data.get("dni"))
    except services.YaRegistrado as ya:
        return Response(
            {
                "detail": "Este DNI ya está preinscrito. Te escribiremos por WhatsApp.",
                "codigo": ya.codigo,
            },
            status=status.HTTP_409_CONFLICT,
        )
    except ErrorDni as err:
        return Response({"detail": err.mensaje}, status=err.status)

    return Response(persona)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VoluntariosThrottle])
def registrar(request):
    """POST /api/voluntarios/ — paso 3 del modal."""
    try:
        voluntario = services.registrar(
            dni=request.data.get("dni"),
            celular=request.data.get("celular"),
            acepta_whatsapp=request.data.get("acepta_whatsapp") is True,
            request=request,
        )
    except services.YaRegistrado as ya:
        return Response(
            {
                "detail": "Este DNI ya está preinscrito. Te escribiremos por WhatsApp.",
                "codigo": ya.codigo,
            },
            status=status.HTTP_409_CONFLICT,
        )
    except ErrorDni as err:
        return Response({"detail": err.mensaje}, status=err.status)

    return Response(serializar_voluntario(voluntario), status=status.HTTP_201_CREATED)
