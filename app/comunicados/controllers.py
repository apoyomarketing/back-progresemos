from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.usuarios.permissions import EsAdministradorOEditor

from . import services


def serializar_comunicado(comunicado, request):
    return {
        "id": comunicado.id,
        "titulo": comunicado.titulo,
        "multimedia": request.build_absolute_uri(comunicado.multimedia.url) if comunicado.multimedia else None,
        "descripcion": comunicado.descripcion,
        "fecha": comunicado.fecha,
        "activo": comunicado.activo,
        "created_at": comunicado.created_at,
        "updated_at": comunicado.updated_at,
    }


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def crear(request):
    comunicado = services.crear_comunicado(request.data, request.FILES)
    return Response(
        serializar_comunicado(comunicado, request),
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def listar(request):
    comunicados = services.listar_comunicados()
    return Response([serializar_comunicado(c, request) for c in comunicados])


@api_view(["GET"])
@permission_classes([AllowAny])
def detalle(request, comunicado_id):
    comunicado = services.obtener_comunicado_publico(comunicado_id)
    return Response(serializar_comunicado(comunicado, request))


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def actualizar(request, comunicado_id):
    comunicado = services.actualizar_comunicado(comunicado_id, request.data, request.FILES)
    return Response(serializar_comunicado(comunicado, request))


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def eliminar(request, comunicado_id):
    services.eliminar_comunicado(comunicado_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
