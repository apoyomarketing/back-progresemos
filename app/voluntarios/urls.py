from django.urls import path

from . import controllers

urlpatterns = [
    path('voluntarios/validar-dni/', controllers.validar_dni, name='voluntarios-validar-dni'),
    path('voluntarios/', controllers.registrar, name='voluntarios-registrar'),
]
