from django.contrib import admin

from .models import Cargo, Candidato


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombres",
        "apellido_paterno",
        "cargo",
        "activo",
        "orden",
    )

    list_filter = (
        "activo",
        "cargo",
    )

    search_fields = (
        "nombres",
        "apellido_paterno",
        "apellido_materno",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
