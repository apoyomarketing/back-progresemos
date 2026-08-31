from datetime import date

from rest_framework.exceptions import NotFound, ValidationError

from .models import Actividad, Asistencia, RolAfiliado


def _parse_fecha(value, default=None):
    if value is None or value == "":
        return default
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        raise ValidationError({"fecha": "fecha debe tener el formato AAAA-MM-DD."})


def listar_roles_afiliado():
    return RolAfiliado.objects.all()


def crear_actividad(data):
    nombre = data.get("nombre")
    descripcion = data.get("descripcion", "")
    tipo = data.get("tipo", "")
    fecha = _parse_fecha(data.get("fecha"))
    lugar = data.get("lugar")
    estado = data.get("estado", Actividad.PROGRAMADO)

    if not nombre:
        raise ValidationError({"nombre": "El nombre es obligatorio."})

    if not fecha:
        raise ValidationError({"fecha": "La fecha es obligatoria."})

    if not lugar:
        raise ValidationError({"lugar": "El lugar es obligatorio."})

    return Actividad.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        tipo=tipo,
        fecha=fecha,
        lugar=lugar,
        estado=estado,
    )


def obtener_actividad(actividad_id):
    try:
        return Actividad.objects.get(pk=actividad_id)
    except Actividad.DoesNotExist:
        raise NotFound("La actividad no existe.")


def actualizar_actividad(actividad_id, data):
    actividad = obtener_actividad(actividad_id)

    if "nombre" in data:
        actividad.nombre = data["nombre"]

    if "descripcion" in data:
        actividad.descripcion = data["descripcion"]

    if "tipo" in data:
        actividad.tipo = data["tipo"]

    if "fecha" in data:
        actividad.fecha = _parse_fecha(data["fecha"], actividad.fecha)

    if "lugar" in data:
        actividad.lugar = data["lugar"]

    if "estado" in data:
        actividad.estado = data["estado"]

    actividad.save()

    return actividad


def eliminar_actividad(actividad_id):
    actividad = obtener_actividad(actividad_id)
    actividad.estado = Actividad.CANCELADO
    actividad.save(update_fields=["estado"])
    return actividad


def listar_actividades():
    return Actividad.objects.exclude(estado=Actividad.CANCELADO)


def crear_asistencia(data):
    voluntario_id = data.get("voluntario_id")
    actividad_id = data.get("actividad_id")
    estado = data.get("estado", Asistencia.PRESENTE)
    observacion = data.get("observacion", "")

    if not voluntario_id:
        raise ValidationError({"voluntario_id": "El voluntario es obligatorio."})

    if not actividad_id:
        raise ValidationError({"actividad_id": "La actividad es obligatoria."})

    # Import diferido: evita el import circular entre voluntarios y asistencia.
    from app.voluntarios.models import Voluntario

    try:
        voluntario = Voluntario.objects.get(pk=voluntario_id)
    except Voluntario.DoesNotExist:
        raise ValidationError({"voluntario_id": "Ese voluntario no existe."})

    actividad = obtener_actividad(actividad_id)

    duplicado = Asistencia.objects.filter(
        voluntario=voluntario, actividad=actividad
    ).exclude(estado=Asistencia.ELIMINADO)
    if duplicado.exists():
        raise ValidationError(
            {"detail": "Ya existe un registro de asistencia para este voluntario en esta actividad."}
        )

    return Asistencia.objects.create(
        voluntario=voluntario,
        actividad=actividad,
        estado=estado,
        observacion=observacion,
    )


def obtener_asistencia(asistencia_id):
    try:
        return Asistencia.objects.get(pk=asistencia_id)
    except Asistencia.DoesNotExist:
        raise NotFound("El registro de asistencia no existe.")


def actualizar_asistencia(asistencia_id, data):
    asistencia = obtener_asistencia(asistencia_id)

    if "estado" in data:
        asistencia.estado = data["estado"]

    if "observacion" in data:
        asistencia.observacion = data["observacion"]

    asistencia.save()

    return asistencia


def eliminar_asistencia(asistencia_id):
    asistencia = obtener_asistencia(asistencia_id)
    asistencia.estado = Asistencia.ELIMINADO
    asistencia.save(update_fields=["estado"])
    return asistencia


def listar_asistencias(actividad_id=None, voluntario_id=None):
    qs = Asistencia.objects.exclude(estado=Asistencia.ELIMINADO)

    if actividad_id:
        qs = qs.filter(actividad_id=actividad_id)

    if voluntario_id:
        qs = qs.filter(voluntario_id=voluntario_id)

    return qs
