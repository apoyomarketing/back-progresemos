from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import services
from .permissions import EsAdministrador


def serializar_usuario(usuario):
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "estado": usuario.estado,
        "is_staff": usuario.is_staff,
        "rol": {
            "id": usuario.rol.id,
            "nombre": usuario.rol.nombre,
        } if usuario.rol else None,
        "created_at": usuario.created_at,
        "updated_at": usuario.updated_at,
    }


@api_view(["POST"])
@permission_classes([EsAdministrador])
def register(request):
    usuario = services.registrar_usuario(request.data)
    tokens = services.generar_tokens(usuario)

    return Response(
        {"usuario": serializar_usuario(usuario), **tokens},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    usuario = services.iniciar_sesion(
        request,
        request.data.get("email"),
        request.data.get("password"),
    )
    tokens = services.generar_tokens(usuario)

    return Response({"usuario": serializar_usuario(usuario), **tokens})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    services.cerrar_sesion(request.data.get("refresh"))
    return Response(status=status.HTTP_205_RESET_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cambiar_password(request):
    services.cambiar_password(
        request.user,
        request.data.get("password_actual"),
        request.data.get("password_nuevo"),
    )
    return Response({"detail": "Contraseña actualizada correctamente."})


@api_view(["GET"])
@permission_classes([EsAdministrador])
def listar_usuarios(request):
    usuarios = services.listar_usuarios()
    return Response([serializar_usuario(u) for u in usuarios])


@api_view(["POST"])
@permission_classes([EsAdministrador])
def actualizar_usuario(request, usuario_id):
    usuario = services.actualizar_usuario(usuario_id, request.data, request.user)
    return Response(serializar_usuario(usuario))


@api_view(["POST"])
@permission_classes([EsAdministrador])
def eliminar_usuario(request, usuario_id):
    usuario = services.eliminar_usuario(usuario_id, request.user)
    return Response(serializar_usuario(usuario))


@api_view(["POST"])
@permission_classes([EsAdministrador])
def resetear_password_usuario(request, usuario_id):
    services.resetear_password_usuario(usuario_id, request.data.get("password_nuevo"), request.user)
    return Response({"detail": "Contraseña actualizada correctamente."})


def serializar_rol(rol):
    return {
        "id": rol.id,
        "nombre": rol.nombre,
        "activo": rol.activo,
        "created_at": rol.created_at,
        "updated_at": rol.updated_at,
    }


@api_view(["POST"])
@permission_classes([EsAdministrador])
def crear_rol(request):
    rol = services.crear_rol(request.data)
    return Response(serializar_rol(rol), status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([EsAdministrador])
def listar_roles(request):
    roles = services.listar_roles()
    return Response([serializar_rol(r) for r in roles])


@api_view(["GET"])
@permission_classes([EsAdministrador])
def detalle_rol(request, rol_id):
    rol = services.obtener_rol_publico(rol_id)
    return Response(serializar_rol(rol))


@api_view(["POST"])
@permission_classes([EsAdministrador])
def actualizar_rol(request, rol_id):
    rol = services.actualizar_rol(rol_id, request.data)
    return Response(serializar_rol(rol))


@api_view(["POST"])
@permission_classes([EsAdministrador])
def eliminar_rol(request, rol_id):
    services.eliminar_rol(rol_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
