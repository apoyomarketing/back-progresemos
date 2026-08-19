from datetime import date

from rest_framework.exceptions import NotFound, ValidationError

from .models import Noticia


def _parse_fecha(value, default):
    if value is None or value == "":
        return default
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        raise ValidationError({"fecha": "fecha debe tener el formato AAAA-MM-DD."})


def _parse_bool(value, default):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "1", "on", "yes")


def crear_noticia(data, archivos):
    titulo = data.get("titulo")
    multimedia = archivos.get("multimedia")
    descripcion = data.get("descripcion", "")
    fecha = _parse_fecha(data.get("fecha"), None)
    lugar = data.get("lugar", "")
    activo = _parse_bool(data.get("activo"), True)

    if not titulo:
        raise ValidationError({"titulo": "El título es obligatorio."})

    return Noticia.objects.create(
        titulo=titulo,
        multimedia=multimedia,
        descripcion=descripcion,
        fecha=fecha,
        lugar=lugar,
        activo=activo,
    )


def obtener_noticia(noticia_id):
    """Búsqueda interna (sin filtrar por activo) para actualizar/eliminar/reactivar."""
    try:
        return Noticia.objects.get(pk=noticia_id)
    except Noticia.DoesNotExist:
        raise NotFound("La noticia no existe.")


def obtener_noticia_publica(noticia_id):
    noticia = obtener_noticia(noticia_id)

    if not noticia.activo:
        raise NotFound("La noticia no existe.")

    return noticia


def actualizar_noticia(noticia_id, data, archivos):
    noticia = obtener_noticia(noticia_id)

    if "titulo" in data:
        noticia.titulo = data["titulo"]

    if "multimedia" in archivos:
        noticia.multimedia = archivos["multimedia"]

    if "descripcion" in data:
        noticia.descripcion = data["descripcion"]

    if "fecha" in data:
        noticia.fecha = _parse_fecha(data["fecha"], noticia.fecha)

    if "lugar" in data:
        noticia.lugar = data["lugar"]

    if "activo" in data:
        noticia.activo = _parse_bool(data["activo"], noticia.activo)

    noticia.save()

    return noticia


def eliminar_noticia(noticia_id):
    noticia = obtener_noticia(noticia_id)
    noticia.activo = False
    noticia.save(update_fields=["activo"])
    return noticia


def listar_noticias():
    return Noticia.objects.filter(activo=True)
