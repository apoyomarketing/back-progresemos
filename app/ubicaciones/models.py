from django.db import models


class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True, db_column='id_departamento')
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True, db_column='id_provincia')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='provincias')
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'provincias'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        unique_together = (('departamento', 'nombre'),)

    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"


class Distrito(models.Model):
    id_distrito = models.AutoField(primary_key=True, db_column='id_distrito')
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='distritos')
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'distritos'
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'
        unique_together = (('provincia', 'nombre'),)

    def __str__(self):
        return f"{self.nombre} ({self.provincia.nombre})"
