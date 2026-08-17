from django.contrib import admin
from .models import Rol, Usuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
    )

    search_fields = (
        "nombre",
    )


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "nombre",
        "rol",
        "estado",
        "is_staff",
    )

    search_fields = (
        "email",
        "nombre",
    )

    list_filter = (
        "rol",
        "estado",
        "is_staff",
    )