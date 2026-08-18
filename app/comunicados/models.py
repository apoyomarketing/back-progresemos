from django.db import models

from app.core.models import TimeStampedModel


class Comunicado(TimeStampedModel):
    titulo = models.CharField(max_length=255)
    multimedia = models.FileField(upload_to="comunicado/", null=True, blank=True)
    descripcion = models.TextField()
    fecha = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "comunicados"
        ordering = ["-fecha", "-created_at"]
        verbose_name = "Comunicado"
        verbose_name_plural = "Comunicados"

    def __str__(self):
        return self.titulo
