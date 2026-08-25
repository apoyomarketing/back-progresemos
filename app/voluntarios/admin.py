from django.contrib import admin

from .models import ConsultaReniec, LimitadorApi, Voluntario


@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ("dni", "nombre_completo", "celular", "estado", "created_at")
    list_filter = ("estado", "acepta_whatsapp", "origen", "created_at")
    search_fields = ("dni", "nombre_completo", "celular", "codigo")
    readonly_fields = ("codigo", "ip", "user_agent", "created_at", "updated_at")
    date_hierarchy = "created_at"

    # No se crean voluntarios a mano: el nombre debe venir siempre de RENIEC.
    def has_add_permission(self, request):
        return False


@admin.register(LimitadorApi)
class LimitadorApiAdmin(admin.ModelAdmin):
    """
    Aquí se recalibra el caudal hacia Decolecta SIN redesplegar.
    Regla: capacidad + tasa debe ser menor que el tope del plan contratado.
    """

    list_display = ("clave", "tasa", "capacidad", "tokens", "actualizado")
    readonly_fields = ("tokens", "actualizado")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsultaReniec)
class ConsultaReniecAdmin(admin.ModelAdmin):
    """Solo lectura: sirve para auditar cuántos créditos se están gastando."""

    list_display = ("dni", "nombre_completo", "updated_at")
    search_fields = ("dni", "nombre_completo")
    readonly_fields = ("dni", "nombres", "apellido_paterno", "apellido_materno",
                       "nombre_completo", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False
