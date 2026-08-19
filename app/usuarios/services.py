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


def obtener_usuario(usuario_id):
    try:
        return Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        raise NotFound("El usuario no existe.")


def actualizar_usuario(usuario_id, data, actor):
    usuario = obtener_usuario(usuario_id)

    if "nombre" in data:
        nombre = data["nombre"]
        if not nombre:
            raise ValidationError({"nombre": "El nombre no puede estar vacío."})
        usuario.nombre = nombre

    if "email" in data:
        email = data["email"]
        if not email:
            raise ValidationError({"email": "El email no puede estar vacío."})
        if Usuario.objects.filter(email__iexact=email).exclude(pk=usuario.pk).exists():
            raise ValidationError({"email": "Ya existe un usuario con este correo."})
        usuario.email = email

    if "rol" in data:
        usuario.rol_id = data["rol"] or None

    if "estado" in data:
        nuevo_estado = _parse_bool(data["estado"], usuario.estado)
        if usuario.pk == actor.id and not nuevo_estado:
            raise ValidationError("No podés desactivarte a vos mismo.")
        usuario.estado = nuevo_estado

    usuario.save()

    return usuario


def eliminar_usuario(usuario_id, actor):
    if usuario_id == actor.id:
        raise ValidationError("No podés eliminarte a vos mismo.")

    usuario = obtener_usuario(usuario_id)
    usuario.estado = False
    usuario.save(update_fields=["estado"])

    return usuario


def resetear_password_usuario(usuario_id, password_nuevo, actor):
    if usuario_id == actor.id:
        raise ValidationError(
            "No podés resetear tu propia contraseña por acá. Usá /usuarios/cambiar-password/."
        )

    usuario = obtener_usuario(usuario_id)

    if not password_nuevo:
        raise ValidationError({"password_nuevo": "La nueva contraseña es obligatoria."})

    if len(password_nuevo) < 8:
        raise ValidationError({"password_nuevo": "La nueva contraseña debe tener al menos 8 caracteres."})

    usuario.set_password(password_nuevo)
    usuario.save(update_fields=["password"])


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
