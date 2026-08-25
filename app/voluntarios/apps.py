from django.apps import AppConfig


class VoluntariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.voluntarios"
    label = "voluntarios"
    verbose_name = "Voluntarios"

    def ready(self):
        from . import checks  # noqa: F401  (registra las comprobaciones)
