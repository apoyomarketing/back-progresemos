from django.db import models

from app.core.models import TimeStampedModel


class Cargo(TimeStampedModel):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "cargos"
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Candidato(TimeStampedModel):
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
        related_name="candidatos",
    )

    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)

    foto = models.ImageField(
        upload_to="candidatos/fotos/",
        null=True,
        blank=True
    )

    descripcion = models.TextField(blank=True)

    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "candidatos"
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"
