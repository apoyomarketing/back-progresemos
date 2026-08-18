from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import Usuario


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
