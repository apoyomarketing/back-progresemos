from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.usuarios.permissions import EsAdministradorOEditor

from . import services


def serializar_propuesta(propuesta, request):
    return {
        "id": propuesta.id,
        "titulo": propuesta.titulo,
        "foto": request.build_absolute_uri(propuesta.foto.url) if propuesta.foto else None,
        "descripcion": propuesta.descripcion,
        "orden": propuesta.orden,
        "activo": propuesta.activo,
        "created_at": propuesta.created_at,
        "updated_at": propuesta.updated_at,
    }


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def crear(request):
    propuesta = services.crear_propuesta(request.data, request.FILES)
    return Response(
        serializar_propuesta(propuesta, request),
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def listar(request):
    propuestas = services.listar_propuestas()
    return Response([serializar_propuesta(p, request) for p in propuestas])


@api_view(["GET"])
@permission_classes([AllowAny])
def detalle(request, propuesta_id):
    propuesta = services.obtener_propuesta_publica(propuesta_id)
    return Response(serializar_propuesta(propuesta, request))


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def actualizar(request, propuesta_id):
    propuesta = services.actualizar_propuesta(propuesta_id, request.data, request.FILES)
    return Response(serializar_propuesta(propuesta, request))


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def eliminar(request, propuesta_id):
    services.eliminar_propuesta(propuesta_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
