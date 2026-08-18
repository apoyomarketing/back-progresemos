from django.urls import path

from . import controllers

urlpatterns = [
    path('usuarios/register/', controllers.register, name='usuarios-register'),
    path('usuarios/login/', controllers.login, name='usuarios-login'),
    path('usuarios/logout/', controllers.logout, name='usuarios-logout'),
    path('usuarios/cambiar-password/', controllers.cambiar_password, name='usuarios-cambiar-password'),
    path('usuarios/', controllers.listar_usuarios, name='usuarios-list'),
]
