from django.db import models


class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True, db_column="id_cargo")
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "cargos"
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.nombre


class Candidato(models.Model):
    id_candidato = models.AutoField(primary_key=True, db_column="id_candidato")

    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
        related_name="candidatos",
        db_column="id_cargo"
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
    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "candidatos"
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"
        ordering = ["orden", "id_candidato"]

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"