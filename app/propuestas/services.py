from rest_framework.exceptions import NotFound, ValidationError

from .models import Propuesta


def _parse_bool(value, default):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "1", "on", "yes")


def _parse_int(value, default):
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError({"orden": "orden debe ser un número entero."})


def crear_propuesta(data, archivos):
    titulo = data.get("titulo")
    foto = archivos.get("foto")
    descripcion = data.get("descripcion", "")
    orden = _parse_int(data.get("orden"), 0)
    activo = _parse_bool(data.get("activo"), True)

    if not titulo:
        raise ValidationError({"titulo": "El título es obligatorio."})

    if not foto:
        raise ValidationError({"foto": "La foto es obligatoria."})

    return Propuesta.objects.create(
        titulo=titulo,
        foto=foto,
        descripcion=descripcion,
        orden=orden,
        activo=activo,
    )


def obtener_propuesta(propuesta_id):
    """Búsqueda interna (sin filtrar por activo) para actualizar/eliminar/reactivar."""
    try:
        return Propuesta.objects.get(pk=propuesta_id)
    except Propuesta.DoesNotExist:
        raise NotFound("La propuesta no existe.")


def obtener_propuesta_publica(propuesta_id):
    propuesta = obtener_propuesta(propuesta_id)

    if not propuesta.activo:
        raise NotFound("La propuesta no existe.")

    return propuesta


def actualizar_propuesta(propuesta_id, data, archivos):
    propuesta = obtener_propuesta(propuesta_id)

    if "titulo" in data:
        propuesta.titulo = data["titulo"]

    if "foto" in archivos:
        propuesta.foto = archivos["foto"]

    if "descripcion" in data:
        propuesta.descripcion = data["descripcion"]

    if "orden" in data:
        propuesta.orden = _parse_int(data["orden"], propuesta.orden)

    if "activo" in data:
        propuesta.activo = _parse_bool(data["activo"], propuesta.activo)

    propuesta.save()

    return propuesta


def eliminar_propuesta(propuesta_id):
    propuesta = obtener_propuesta(propuesta_id)
    propuesta.activo = False
    propuesta.save(update_fields=["activo"])
    return propuesta


def listar_propuestas():
    return Propuesta.objects.filter(activo=True)
