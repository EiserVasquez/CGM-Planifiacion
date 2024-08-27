from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('lista_reservas/', views.lista_reservas, name='lista_reservas'),
    path('plan-limpiartablas/', views.limpiar_tablasplan, name='plan-limpiartablas'),
    path('plan-reservas/', views.crear_planreservas, name='plan-reservas'),
    path('plan-avisorden/', views.crear_planavisorden, name='plan-avisorden'),
    path('plan-ordenes/', views.crear_planordenes, name='plan-ordenes'),
    path('plan-crear/', views.crear_planabastecimiento, name='plan-crear'),
    path('plan-pruebas/', views.crear_pruebas, name='plan-pruebas'),
]
