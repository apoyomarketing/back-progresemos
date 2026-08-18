from django.db import models

from app.core.models import TimeStampedModel


class Noticia(TimeStampedModel):
    titulo = models.CharField(max_length=255)
    multimedia = models.FileField(upload_to="noticia/", null=True, blank=True)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(null=True, blank=True)
    lugar = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "noticias"
        ordering = ["-fecha", "-created_at"]
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

    def __str__(self):
        return self.titulo
