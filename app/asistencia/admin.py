from django.contrib import admin

from .models import Actividad, Asistencia, RolAfiliado


@admin.register(RolAfiliado)
class RolAfiliadoAdmin(admin.ModelAdmin):
    list_display = ("rol_name",)
    search_fields = ("rol_name",)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "fecha", "lugar", "estado")
    list_filter = ("estado", "tipo", "fecha")
    search_fields = ("nombre", "lugar")
    date_hierarchy = "fecha"


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("voluntario", "actividad", "estado", "created_at")
    list_filter = ("estado", "actividad")
    search_fields = ("voluntario__dni", "voluntario__nombre_completo")
    date_hierarchy = "created_at"
