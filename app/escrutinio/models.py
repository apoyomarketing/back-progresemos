from django.db import models
from django.core.exceptions import ValidationError

class LocalVotacion(models.Model):
    id_local = models.IntegerField(primary_key=True)
    provincia = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50)
    nombre_local = models.CharField(max_length=150)
    direccion_local = models.CharField(max_length=200, blank=True, null=True)
    cant_mesas = models.PositiveIntegerField()
    electores_regional = models.PositiveIntegerField()
    extranjeros_inscritos = models.PositiveIntegerField(default=0)
    electores_municipal = models.PositiveIntegerField()
    localidades_msi = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'local_votacion'
        verbose_name_plural = 'Locales de Votación'

    def __str__(self):
        return f"{self.nombre_local} - {self.distrito}"

class Partido(models.Model):
    id_partido = models.AutoField(primary_key=True)
    nombre_partido = models.CharField(max_length=150, unique=True)
    categoria = models.CharField(max_length=10, default='PARTIDO')

    class Meta:
        db_table = 'partido'

    def __str__(self):
        return self.nombre_partido

class Voto(models.Model):
    TIPO_ELECCION_CHOICES = [
        ('REGIONAL', 'Regional'),
        ('CONSEJERO', 'Consejero Regional'),
        ('PROVINCIAL', 'Provincial'),
        ('DISTRITAL', 'Distrital'),
    ]

    id_voto = models.AutoField(primary_key=True)
    local = models.ForeignKey(LocalVotacion, on_delete=models.CASCADE, db_column='id_local', related_name='votos')
    nro_mesa = models.CharField(max_length=20)
    tipo_eleccion = models.CharField(max_length=20, choices=TIPO_ELECCION_CHOICES)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, db_column='id_partido')
    cant_voto = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'voto'
        unique_together = ('local', 'nro_mesa', 'tipo_eleccion', 'partido')
        # Nota: nro_mesa debe ser único globalmente entre mesas del mismo tipo_eleccion.
        # Esta validación se aplica en el servicio (validate_nro_mesa_unico).

    def __str__(self):
        return f"{self.cant_voto} votos - {self.partido.nombre_partido} - Mesa {self.nro_mesa} ({self.tipo_eleccion})"
