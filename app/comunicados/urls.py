from django.urls import path

from . import controllers

urlpatterns = [
    path('comunicados/crear/', controllers.crear, name='comunicados-crear'),
    path('comunicados/<int:comunicado_id>/actualizar/', controllers.actualizar, name='comunicados-actualizar'),
    path('comunicados/<int:comunicado_id>/eliminar/', controllers.eliminar, name='comunicados-eliminar'),
    path('comunicados/<int:comunicado_id>/', controllers.detalle, name='comunicados-detalle'),
    path('comunicados/', controllers.listar, name='comunicados-list'),
]
