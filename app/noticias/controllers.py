from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.usuarios.permissions import EsAdministradorOEditor

from . import services


def serializar_noticia(noticia, request):
    return {
        "id": noticia.id,
        "titulo": noticia.titulo,
        "multimedia": request.build_absolute_uri(noticia.multimedia.url) if noticia.multimedia else None,
        "descripcion": noticia.descripcion,
        "fecha": noticia.fecha,
        "lugar": noticia.lugar,
        "activo": noticia.activo,
        "created_at": noticia.created_at,
        "updated_at": noticia.updated_at,
    }


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def crear(request):
    noticia = services.crear_noticia(request.data, request.FILES)
    return Response(
        serializar_noticia(noticia, request),
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def listar(request):
    noticias = services.listar_noticias()
    return Response([serializar_noticia(n, request) for n in noticias])


@api_view(["GET"])
@permission_classes([AllowAny])
def detalle(request, noticia_id):
    noticia = services.obtener_noticia_publica(noticia_id)
    return Response(serializar_noticia(noticia, request))


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def actualizar(request, noticia_id):
    noticia = services.actualizar_noticia(noticia_id, request.data, request.FILES)
    return Response(serializar_noticia(noticia, request))


@api_view(["POST"])
@permission_classes([EsAdministradorOEditor])
def eliminar(request, noticia_id):
    services.eliminar_noticia(noticia_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
