from django.db import models

from app.core.models import TimeStampedModel


class Propuesta(TimeStampedModel):
    titulo = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="propuesta/")
    descripcion = models.TextField(blank=True)

    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "propuestas"
        ordering = ["orden", "-created_at"]
        verbose_name = "Propuesta"
        verbose_name_plural = "Propuestas"

    def __str__(self):
        return self.titulo
