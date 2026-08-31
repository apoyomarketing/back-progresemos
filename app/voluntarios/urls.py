from django.urls import path

from . import controllers

urlpatterns = [
    path('voluntarios/validar-dni/', controllers.validar_dni, name='voluntarios-validar-dni'),
    path('voluntarios/buscar/', controllers.buscar, name='voluntarios-buscar'),
    path('voluntarios/<str:codigo>/foto/', controllers.subir_foto, name='voluntarios-foto'),
    path('voluntarios/<str:codigo>/rol/', controllers.actualizar_rol, name='voluntarios-rol'),
    path('voluntarios/<str:codigo>/eliminar/', controllers.eliminar, name='voluntarios-eliminar'),
    path('voluntarios/<str:dni>/', controllers.obtener_por_dni, name='voluntarios-detalle'),
    path('voluntarios/', controllers.registrar, name='voluntarios-registrar'),
]
