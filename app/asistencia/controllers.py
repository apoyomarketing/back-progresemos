from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from app.usuarios.permissions import EsAdministradorEditorOCoordinador

from . import services


def serializar_rol_afiliado(rol):
    return {
        "id": rol.id,
        "rol_name": rol.rol_name,
    }


def serializar_actividad(actividad):
    return {
        "id": actividad.id,
        "nombre": actividad.nombre,
        "descripcion": actividad.descripcion,
        "tipo": actividad.tipo,
        "fecha": actividad.fecha,
        "lugar": actividad.lugar,
        "estado": actividad.estado,
    }


def serializar_asistencia(asistencia):
    return {
        "id": asistencia.id,
        "voluntario_id": asistencia.voluntario_id,
        "actividad_id": asistencia.actividad_id,
        "estado": asistencia.estado,
        "observacion": asistencia.observacion,
        "created_at": asistencia.created_at,
    }


@api_view(["GET"])
@permission_classes([EsAdministradorEditorOCoordinador])
def listar_roles_afiliado(request):
    roles = services.listar_roles_afiliado()
    return Response([serializar_rol_afiliado(r) for r in roles])


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def crear_actividad(request):
    actividad = services.crear_actividad(request.data)
    return Response(serializar_actividad(actividad), status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([EsAdministradorEditorOCoordinador])
def listar_actividades(request):
    actividades = services.listar_actividades()
    return Response([serializar_actividad(a) for a in actividades])


@api_view(["GET"])
@permission_classes([EsAdministradorEditorOCoordinador])
def detalle_actividad(request, actividad_id):
    actividad = services.obtener_actividad(actividad_id)
    return Response(serializar_actividad(actividad))


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def actualizar_actividad(request, actividad_id):
    actividad = services.actualizar_actividad(actividad_id, request.data)
    return Response(serializar_actividad(actividad))


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def eliminar_actividad(request, actividad_id):
    actividad = services.eliminar_actividad(actividad_id)
    return Response(serializar_actividad(actividad))


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def crear_asistencia(request):
    asistencia = services.crear_asistencia(request.data)
    return Response(serializar_asistencia(asistencia), status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([EsAdministradorEditorOCoordinador])
def listar_asistencias(request):
    asistencias = services.listar_asistencias(
        actividad_id=request.query_params.get("actividad_id"),
        voluntario_id=request.query_params.get("voluntario_id"),
    )
    return Response([serializar_asistencia(a) for a in asistencias])


@api_view(["GET"])
@permission_classes([EsAdministradorEditorOCoordinador])
def detalle_asistencia(request, asistencia_id):
    asistencia = services.obtener_asistencia(asistencia_id)
    return Response(serializar_asistencia(asistencia))


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def actualizar_asistencia(request, asistencia_id):
    asistencia = services.actualizar_asistencia(asistencia_id, request.data)
    return Response(serializar_asistencia(asistencia))


@api_view(["POST"])
@permission_classes([EsAdministradorEditorOCoordinador])
def eliminar_asistencia(request, asistencia_id):
    asistencia = services.eliminar_asistencia(asistencia_id)
    return Response(serializar_asistencia(asistencia))
