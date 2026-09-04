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

from app.usuarios.permissions import EsAdministradorEditorOCoordinador

from . import services
from .decolecta import ErrorDni


class VoluntariosThrottle(AnonRateThrottle):
    """Límite por IP. La tasa vive en REST_FRAMEWORK.DEFAULT_THROTTLE_RATES."""

    scope = "voluntarios"


def serializar_voluntario(voluntario, request):
    return {
        "codigo": voluntario.codigo,
        "dni": voluntario.dni,
        "nombre_completo": voluntario.nombre_completo,
        "estado": voluntario.estado,
        "foto": request.build_absolute_uri(voluntario.foto.url) if voluntario.foto else None,
        "fecha_afiliacion": voluntario.created_at,
    }


def serializar_voluntario_admin(voluntario, request):
    """Igual que serializar_voluntario pero con el id interno y el rol de afiliado —
    solo para vistas de staff (buscar/, rol/, eliminar/), que necesitan el id como
    voluntario_id al pasar asistencia y el rol para poder mostrarlo/editarlo. No se
    usa en los endpoints públicos para no exponer el PK ahí."""
    return {
        "id": voluntario.id,
        "rol_afiliado": voluntario.rol_afiliado.rol_name,
        **serializar_voluntario(voluntario, request),
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

    return Response(serializar_voluntario(voluntario, request), status=status.HTTP_201_CREATED)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VoluntariosThrottle])
def subir_foto(request, codigo):
    """POST /api/voluntarios/<codigo>/foto/ — sube la foto para el carnet."""
    voluntario = services.guardar_foto(codigo, request.FILES.get("foto"))
    return Response(serializar_voluntario(voluntario, request))


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VoluntariosThrottle])
def actualizar_foto(request, dni):
    """POST /api/voluntarios/<dni>/actualizar-foto/ — reemplaza la foto de un voluntario ya registrado."""
    voluntario = services.actualizar_foto_por_dni(dni, request.FILES.get("foto"))
    return Response(serializar_voluntario(voluntario, request))


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([VoluntariosThrottle])
def obtener_por_dni(request, dni):
    """GET /api/voluntarios/<dni>/ — regenerar el carnet sin volver a registrarse."""
    voluntario = services.obtener_voluntario_por_dni(dni)
    return Response(serializar_voluntario(voluntario, request))


@api_view(["GET"])
@permission_classes([EsAdministradorEditorOCoordinador])
def buscar(request):
    """GET /api/voluntarios/buscar/?nombre=&dni= — búsqueda interna (staff)."""
    voluntarios = services.buscar_voluntarios(
        nombre=request.query_params.get("nombre"),
        dni=request.query_params.get("dni"),
    )
    return Response([serializar_voluntario_admin(v, request) for v in voluntarios])


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def actualizar_rol(request, codigo):
    """POST /api/voluntarios/<codigo>/rol/ — cambia el rol de afiliado (staff).

    El catálogo de roles (RolAfiliado) está pensado como de solo lectura por API
    ("se administra desde el admin de Django" — ver app/asistencia/models.py), pero
    el CMS necesita reasignar el rol de un afiliado puntual (p. ej. de simpatizante
    a organizador), no crear/editar el catálogo en sí, así que este endpoint solo
    reasigna la FK de un Voluntario existente a un rol ya existente del catálogo.
    """
    voluntario = services.actualizar_rol_afiliado(codigo, request.data.get("rol_afiliado"))
    return Response(serializar_voluntario_admin(voluntario, request))


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def eliminar(request, codigo):
    """POST /api/voluntarios/<codigo>/eliminar/ — baja lógica (staff)."""
    voluntario = services.eliminar(codigo)
    return Response(serializar_voluntario_admin(voluntario, request))
