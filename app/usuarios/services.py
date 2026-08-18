from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import Rol, Usuario


def _parse_bool(value, default):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "1", "on", "yes")


def generar_tokens(usuario):
    refresh = RefreshToken.for_user(usuario)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def registrar_usuario(data):
    email = data.get("email")
    nombre = data.get("nombre")
    password = data.get("password")
    rol = data.get("rol")

    if not email or not nombre or not password:
        raise ValidationError("nombre, email y password son obligatorios.")

    if len(password) < 8:
        raise ValidationError({"password": "La contraseña debe tener al menos 8 caracteres."})

    if Usuario.objects.filter(email__iexact=email).exists():
        raise ValidationError({"email": "Ya existe un usuario con este correo."})

    return Usuario.objects.create_user(
        email=email,
        nombre=nombre,
        password=password,
        rol_id=rol,
    )


def iniciar_sesion(request, email, password):
    if not email or not password:
        raise ValidationError("email y password son obligatorios.")

    usuario = authenticate(request, email=email, password=password)

    if usuario is None:
        raise AuthenticationFailed("Credenciales inválidas.")

    if not usuario.estado:
        raise AuthenticationFailed("El usuario está inactivo.")

    return usuario


def cerrar_sesion(refresh_token):
    if not refresh_token:
        raise ValidationError("El refresh token es obligatorio.")

    try:
        RefreshToken(refresh_token).blacklist()
    except TokenError:
        raise ValidationError("El refresh token no es válido.")


def cambiar_password(usuario, password_actual, password_nuevo):
    if not password_actual or not password_nuevo:
        raise ValidationError("La contraseña actual y la nueva son obligatorias.")

    if not usuario.check_password(password_actual):
        raise ValidationError({"password_actual": "La contraseña actual es incorrecta."})

    if len(password_nuevo) < 8:
        raise ValidationError({"password_nuevo": "La nueva contraseña debe tener al menos 8 caracteres."})

    usuario.set_password(password_nuevo)
    usuario.save(update_fields=["password"])


def listar_usuarios():
    return Usuario.objects.select_related("rol").all().order_by("id")


def crear_rol(data):
    nombre = data.get("nombre")

    if not nombre:
        raise ValidationError({"nombre": "El nombre es obligatorio."})

    if Rol.objects.filter(nombre__iexact=nombre).exists():
        raise ValidationError({"nombre": "Ya existe un rol con este nombre."})

    return Rol.objects.create(nombre=nombre)


def listar_roles():
    return Rol.objects.filter(activo=True).order_by("nombre")


def obtener_rol(rol_id):
    """Búsqueda interna (sin filtrar por activo) para actualizar/eliminar/reactivar."""
    try:
        return Rol.objects.get(pk=rol_id)
    except Rol.DoesNotExist:
        raise NotFound("El rol no existe.")


def obtener_rol_publico(rol_id):
    rol = obtener_rol(rol_id)

    if not rol.activo:
        raise NotFound("El rol no existe.")

    return rol


def actualizar_rol(rol_id, data):
    rol = obtener_rol(rol_id)
    nombre = data.get("nombre")

    if nombre:
        if Rol.objects.filter(nombre__iexact=nombre).exclude(pk=rol.pk).exists():
            raise ValidationError({"nombre": "Ya existe un rol con este nombre."})

        rol.nombre = nombre

    if "activo" in data:
        rol.activo = _parse_bool(data["activo"], rol.activo)

    rol.save()

    return rol


def eliminar_rol(rol_id):
    rol = obtener_rol(rol_id)
    rol.activo = False
    rol.save(update_fields=["activo"])
