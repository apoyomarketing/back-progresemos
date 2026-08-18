from rest_framework.permissions import BasePermission

ADMINISTRADOR = "Administrador"
EDITOR = "Editor"


def _nombre_rol(usuario):
    return usuario.rol.nombre if usuario.rol else None


def _es_administrador(usuario):
    # is_superuser es la vía de escape para el primer admin (creado por
    # createsuperuser), que todavía no tiene un Rol asignado.
    return usuario.is_superuser or _nombre_rol(usuario) == ADMINISTRADOR


class EsAdministrador(BasePermission):
    message = "Se requiere el rol Administrador."

    def has_permission(self, request, view):
        usuario = request.user
        return bool(usuario and usuario.is_authenticated and _es_administrador(usuario))


class EsAdministradorOEditor(BasePermission):
    message = "Se requiere el rol Administrador o Editor."

    def has_permission(self, request, view):
        usuario = request.user

        if not (usuario and usuario.is_authenticated):
            return False

        return _es_administrador(usuario) or _nombre_rol(usuario) == EDITOR
