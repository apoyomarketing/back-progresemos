from datetime import date

from rest_framework.exceptions import NotFound, ValidationError

from .models import Comunicado


def _parse_bool(value, default):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "1", "on", "yes")


def _parse_fecha(value, default):
    if value is None or value == "":
        return default
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        raise ValidationError({"fecha": "fecha debe tener el formato AAAA-MM-DD."})


def crear_comunicado(data, archivos):
    titulo = data.get("titulo")
    multimedia = archivos.get("multimedia")
    descripcion = data.get("descripcion")
    fecha = _parse_fecha(data.get("fecha"), None)
    activo = _parse_bool(data.get("activo"), True)

    if not titulo:
        raise ValidationError({"titulo": "El título es obligatorio."})

    if not descripcion:
        raise ValidationError({"descripcion": "La descripción es obligatoria."})

    return Comunicado.objects.create(
        titulo=titulo,
        multimedia=multimedia,
        descripcion=descripcion,
        fecha=fecha,
        activo=activo,
    )


def obtener_comunicado(comunicado_id):
    """Búsqueda interna (sin filtrar por activo) para actualizar/eliminar/reactivar."""
    try:
        return Comunicado.objects.get(pk=comunicado_id)
    except Comunicado.DoesNotExist:
        raise NotFound("El comunicado no existe.")


def obtener_comunicado_publico(comunicado_id):
    comunicado = obtener_comunicado(comunicado_id)

    if not comunicado.activo:
        raise NotFound("El comunicado no existe.")

    return comunicado


def actualizar_comunicado(comunicado_id, data, archivos):
    comunicado = obtener_comunicado(comunicado_id)

    if "titulo" in data:
        comunicado.titulo = data["titulo"]

    if "multimedia" in archivos:
        comunicado.multimedia = archivos["multimedia"]

    if "descripcion" in data:
        comunicado.descripcion = data["descripcion"]

    if "fecha" in data:
        comunicado.fecha = _parse_fecha(data["fecha"], comunicado.fecha)

    if "activo" in data:
        comunicado.activo = _parse_bool(data["activo"], comunicado.activo)

    comunicado.save()

    return comunicado


def eliminar_comunicado(comunicado_id):
    comunicado = obtener_comunicado(comunicado_id)
    comunicado.activo = False
    comunicado.save(update_fields=["activo"])
    return comunicado


def listar_comunicados():
    return Comunicado.objects.filter(activo=True)
