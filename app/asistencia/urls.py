from django.urls import path

from . import controllers

urlpatterns = [
    path('afiliado-rol/', controllers.listar_roles_afiliado, name='afiliado-rol-list'),

    path('actividades/crear/', controllers.crear_actividad, name='actividades-crear'),
    path('actividades/<int:actividad_id>/actualizar/', controllers.actualizar_actividad, name='actividades-actualizar'),
    path('actividades/<int:actividad_id>/eliminar/', controllers.eliminar_actividad, name='actividades-eliminar'),
    path('actividades/<int:actividad_id>/', controllers.detalle_actividad, name='actividades-detalle'),
    path('actividades/', controllers.listar_actividades, name='actividades-list'),

    path('asistencia/crear/', controllers.crear_asistencia, name='asistencia-crear'),
    path('asistencia/<int:asistencia_id>/actualizar/', controllers.actualizar_asistencia, name='asistencia-actualizar'),
    path('asistencia/<int:asistencia_id>/eliminar/', controllers.eliminar_asistencia, name='asistencia-eliminar'),
    path('asistencia/<int:asistencia_id>/', controllers.detalle_asistencia, name='asistencia-detalle'),
    path('asistencia/', controllers.listar_asistencias, name='asistencia-list'),
]
