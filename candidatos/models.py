from django.db import models

from django.db import models

class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True, db_column='id_cargo')
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'cargos'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.nombre

class Candidato(models.Model):
    id_candidato = models.AutoField(primary_key=True, db_column='id_candidato')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='candidatos')
    foto = models.ImageField(upload_to='candidatos/fotos/', null=True, blank=True)
    biografia = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'candidatos'
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'
        unique_together = (('nombre', 'apellido', 'cargo'),)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo.nombre}"
