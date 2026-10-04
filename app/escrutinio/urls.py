from django.urls import path
from . import controllers

urlpatterns = [
    path('locales/', controllers.listar_locales, name='listar_locales'),
    path('partidos/', controllers.gestionar_partidos, name='gestionar_partidos'),
    path('votos/', controllers.registrar_votos, name='registrar_votos'),
    path('matriz/', controllers.obtener_matriz, name='obtener_matriz'),
    path('resultados/dashboard/', controllers.resultados_dashboard, name='resultados_dashboard'),
    path('resultados/provincial/', controllers.resultados_provinciales, name='resultados_provinciales'),
    path('resultados/local/<int:id_local>/', controllers.resultados_local, name='resultados_local'),
    path('cobertura/', controllers.cobertura_mesas, name='cobertura_mesas'),
]
