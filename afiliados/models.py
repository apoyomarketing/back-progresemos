from django.db import models
from django.conf import settings


class Afiliado(models.Model):
    dni = models.CharField(
        max_length=8,
        unique=True
    )

    nombres = models.CharField(
        max_length=150
    )

    apellido_paterno = models.CharField(
        max_length=100
    )

    apellido_materno = models.CharField(
        max_length=100
    )

    codigo_carnet = models.CharField(
        max_length=50,
        unique=True
    )

    cargo = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    departamento = models.CharField(
        max_length=100
    )

    provincia = models.CharField(
        max_length=100
    )

    distrito = models.CharField(
        max_length=100
    )

    foto = models.ImageField(
        upload_to="afiliados/",
        blank=True,
        null=True
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="afiliados_registrados"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "afiliados"
        verbose_name = "Afiliado"
        verbose_name_plural = "Afiliados"
        ordering = ["apellido_paterno", "apellido_materno", "nombres"]

    def __str__(self):
        return f"{self.dni} - {self.nombres} {self.apellido_paterno}"