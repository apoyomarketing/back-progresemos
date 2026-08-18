from django.urls import path

from . import controllers

urlpatterns = [
    path('usuarios/register/', controllers.register, name='usuarios-register'),
    path('usuarios/login/', controllers.login, name='usuarios-login'),
    path('usuarios/logout/', controllers.logout, name='usuarios-logout'),
    path('usuarios/cambiar-password/', controllers.cambiar_password, name='usuarios-cambiar-password'),
    path('usuarios/', controllers.listar_usuarios, name='usuarios-list'),

    path('roles/crear/', controllers.crear_rol, name='roles-crear'),
    path('roles/<int:rol_id>/actualizar/', controllers.actualizar_rol, name='roles-actualizar'),
    path('roles/<int:rol_id>/eliminar/', controllers.eliminar_rol, name='roles-eliminar'),
    path('roles/<int:rol_id>/', controllers.detalle_rol, name='roles-detalle'),
    path('roles/', controllers.listar_roles, name='roles-list'),
]
