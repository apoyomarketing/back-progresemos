from django.db import models

from app.core.models import TimeStampedModel


class RolAfiliado(models.Model):
    """Catálogo fijo de roles de afiliado. Sin escritura por API — se administra desde el admin de Django."""

    AFILIADO = "afiliado"
    ORGANIZADOR = "organizador"
    SIMPATIZANTE = "simpatizante"

    rol_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "afiliado_rol"
        verbose_name = "Rol de afiliado"
        verbose_name_plural = "Roles de afiliado"

    def __str__(self):
        return self.rol_name


class Actividad(TimeStampedModel):
    PROGRAMADO = "programado"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"
    ESTADOS = [
        (PROGRAMADO, "Programado"),
        (EN_CURSO, "En curso"),
        (FINALIZADO, "Finalizado"),
        (CANCELADO, "Cancelado"),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=40, blank=True)
    fecha = models.DateField()
    lugar = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=PROGRAMADO)

    class Meta:
        db_table = "actividades"
        ordering = ["-fecha"]
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

    def __str__(self):
        return self.nombre


class Asistencia(TimeStampedModel):
    """Registro de asistencia de un voluntario a una actividad."""

    PRESENTE = "presente"
    AUSENTE = "ausente"
    JUSTIFICADO = "justificado"
    ELIMINADO = "eliminado"
    ESTADOS = [
        (PRESENTE, "Presente"),
        (AUSENTE, "Ausente"),
        (JUSTIFICADO, "Justificado"),
        (ELIMINADO, "Eliminado"),
    ]

    voluntario = models.ForeignKey(
        "voluntarios.Voluntario", on_delete=models.CASCADE, related_name="asistencias"
    )
    actividad = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, related_name="asistencias"
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default=PRESENTE)
    observacion = models.TextField(blank=True)

    class Meta:
        db_table = "voluntarios_asistencia"
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"

    def __str__(self):
        return f"{self.voluntario_id} @ {self.actividad_id} ({self.estado})"
