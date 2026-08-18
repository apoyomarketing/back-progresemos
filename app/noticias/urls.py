from django.urls import path

from . import controllers

urlpatterns = [
    path('noticias/crear/', controllers.crear, name='noticias-crear'),
    path('noticias/<int:noticia_id>/actualizar/', controllers.actualizar, name='noticias-actualizar'),
    path('noticias/<int:noticia_id>/eliminar/', controllers.eliminar, name='noticias-eliminar'),
    path('noticias/<int:noticia_id>/', controllers.detalle, name='noticias-detalle'),
    path('noticias/', controllers.listar, name='noticias-list'),
]
