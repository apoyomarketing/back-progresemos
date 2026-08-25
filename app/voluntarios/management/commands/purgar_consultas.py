"""
Borra consultas a RENIEC antiguas de la caché.

La tabla voluntarios_consulta_reniec guarda nombres de personas que
consultaron su DNI pero quizá nunca completaron el registro. No hay motivo
para conservarlos más allá de su utilidad como caché.

Uso:
    python manage.py purgar_consultas
    python manage.py purgar_consultas --horas 72

Conviene dejarlo como tarea programada diaria en Coolify.
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from app.voluntarios.models import ConsultaReniec, Voluntario


class Command(BaseCommand):
    help = "Purga consultas a RENIEC más antiguas que N horas."

    def add_arguments(self, parser):
        parser.add_argument("--horas", type=int, default=24)

    def handle(self, *args, **opciones):
        limite = timezone.now() - timedelta(hours=opciones["horas"])

        # Los ya registrados no se tocan: su nombre vive en la tabla
        # voluntarios de todas formas.
        registrados = Voluntario.objects.values_list("dni", flat=True)

        borradas, _ = (
            ConsultaReniec.objects.filter(updated_at__lt=limite)
            .exclude(dni__in=registrados)
            .delete()
        )
        self.stdout.write(self.style.SUCCESS(f"Consultas purgadas: {borradas}"))
