from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('lista_reservas/', views.lista_reservas, name='lista_reservas'),
    path('crear_previos/', views.crear_previos, name='crear_previos'),
    path('crear_planreservas/', views.crear_planreservas, name='crear_planreservas'),
    path('crear_planavisorden/', views.crear_planavisorden, name='crear_planavisorden'),
    
]
