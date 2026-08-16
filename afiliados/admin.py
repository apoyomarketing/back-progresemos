from django.contrib import admin
from .models import Afiliado


@admin.register(Afiliado)
class AfiliadoAdmin(admin.ModelAdmin):
    list_display = (
        "dni",
        "nombres",
        "apellido_paterno",
        "apellido_materno",
        "codigo_carnet",
        "departamento",
        "provincia",
        "distrito",
    )

    search_fields = (
        "dni",
        "nombres",
        "apellido_paterno",
        "apellido_materno",
        "codigo_carnet",
    )

    list_filter = (
        "departamento",
        "provincia",
        "distrito",
    )