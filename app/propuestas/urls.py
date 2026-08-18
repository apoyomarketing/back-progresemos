from django.urls import path

from . import controllers

urlpatterns = [
    path('propuestas/crear/', controllers.crear, name='propuestas-crear'),
    path('propuestas/<int:propuesta_id>/actualizar/', controllers.actualizar, name='propuestas-actualizar'),
    path('propuestas/<int:propuesta_id>/eliminar/', controllers.eliminar, name='propuestas-eliminar'),
    path('propuestas/<int:propuesta_id>/', controllers.detalle, name='propuestas-detalle'),
    path('propuestas/', controllers.listar, name='propuestas-list'),
]
