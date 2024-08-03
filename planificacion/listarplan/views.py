from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.db import connection
import pandas as pd

from .models import Avisorden
from .models import Flota
from .models import InventarioS4
from .models import Ordenreserva
from .models import PlanAvisorden
from .models import PlanOrdenreserva
from .models import PlanReservas
from .models import Reservas

# Create your views here.
def index(request):
    return render(request,"index.html")

def lista_reservas(request):
    reservas = list(PlanReservas.objects.values())
    data={'reservas':reservas}
    return JsonResponse(data)

def lista_ordenes(request):
    ordenes = list(PlanAvisorden.objects.values())
    data={'ordenes':ordenes}
    return JsonResponse(data)

def crear_planreservas(request):
    with connection.cursor() as cursor:
        cursor.callproc('abastece_planreservas')
    return HttpResponse("Tabla: Plan Reservas Creada")

def crear_planavisorden(request):
    with connection.cursor() as cursor:
        cursor.callproc('abastece_planavisorden')
    return HttpResponse("Tabla: Plan Aviso Orden Creada")
     
def crear_previos(_request):
    creado = False
    try:
        # with connection.cursor() as cursor:
        #     cursor.callproc('limpieza_tablas_plan')
        #     cursor.callproc('abastece_planreservas')
        #     cursor.callproc('abastece_planavisorden')
            
            # cursor.callproc('abastece_planordenreserva')
            # cursor.callproc('abastece_planaccion')
        # creado = True
        # data = HttpResponse("Tablas: Ordenes y Reservas creadas....")
        # reservas = list(PlanReservas.objects.values())
        # ordenes = list(PlanAvisorden.objects.values())
        
        reservas = pd.DataFrame(PlanReservas.objects.values())
        ordenes = pd.DataFrame(PlanAvisorden.objects.values())
        qreservas = len(reservas)
        qordenes = len(ordenes)
       
        ordenreservas = reservas
        ordenreservas.merge(ordenes, on="orden", how="left", suffixes=("_1","_2"))
        qordenreservas = len(ordenreservas)
        
        print(f'Reservas: {qreservas}')
        print(f'Ordenes: {qordenes}')
        print(f'OrdenReservas: {qordenreservas}')
        
        print(f'Datos OrdenReserva: {ordenreservas}')
                
        # for reserva in reservas:
        #     for orden in ordenes:                
        # valores = {'reservas':qreservas,'ordenes':qordenes,'ordenreservas':qordenreservas}
        valores = qordenreservas.values.tolist()
        # valores = {'reservas':qreservas,'ordenes':qordenes}
         
    except Exception as ex:
        creado = False
        valores = HttpResponse("Error: {ex}")
    return JsonResponse(valores)
