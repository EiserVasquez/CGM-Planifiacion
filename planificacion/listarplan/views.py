from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.db import connection
import pandas as pd
import seaborn as sns
import numpy as np
# import seaborn as sns

from .models import Avisorden, PlanOrdenes
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

# --------------------------------
# PLANEAMIENTO DEL ABASTECIMIENTO
# --------------------------------
# II. Borrar las tablas para el Planeamiento
# III. Tabla: Reservas, Obtener los ultimos registros de las necesidades en Tabla: plan_reservas
# IV. Tabla: AvisoOrdenes, Obtener los ultimos registros de las necesidades en Tabla: plan_avisorden
# V. Tabla: Ordenes, Obtener los ultimos registros de las necesidades en Tabla: plan_ordenes
# VI. Realizar el planeamiento en la Tabla: plan_ordenesreservas




# II. Borrar las tablas para el Planeamiento
# Llamar al procedimiento almacenado limpieza_tablas_plan, en Mysql
# esta considerado borrar las tablas: plan_reservas, plan_avisorden, plan_ordenes, plan_ordenesreservas
# para llenarlas con valores mas recientes de las necesidades en los pasos siguientes
def limpiar_tablasplan(request):
    valores = {}
    valores["estado"] = False
    valores["modo"] = "Ejecutar Procedimiento Myqsl"
    valores["detalle"] = "abastece_limpieza_tablas"
    try:
        with connection.cursor() as cursor:
            cursor.callproc('abastece_limpieza_tablas')
            valores["estado"] = True
    except Exception as error:
        print("Error: ", type(error).__name__, "–", error)
        valores = "Error: " + str(error)
    return JsonResponse(valores, safe=False)


# III. Tabla: Reservas, Obtener los ultimos registros de las necesidades en Tabla: plan_reservas
def crear_planreservas(request):
    valores = {}
    valores["estado"] = False
    valores["modo"] = "Ejecutar Procedimiento Myqsl"
    valores["detalle"] = "abastece_planreservas"
    try:
        with connection.cursor() as cursor:
                cursor.callproc('abastece_planreservas')
                valores["estado"] = True
    except Exception as error:
        print("Error: ", type(error).__name__, "–", error)
        valores = "Error: " + str(error)
    return JsonResponse(valores, safe=False)


# IV. Tabla: AvisoOrdenes, Obtener los ultimos registros de las necesidades en Tabla: plan_avisorden
def crear_planavisorden(request):
    valores = {}
    valores["estado"] = False
    valores["modo"] = "Ejecutar Procedimiento Myqsl"
    valores["detalle"] = "abastece_planavisorden"
    try:
        with connection.cursor() as cursor:
                cursor.callproc('abastece_planavisorden')
                valores["estado"] = True
    except Exception as error:
        print("Error: ", type(error).__name__, "–", error)
        valores = "Error: " + str(error)
    return JsonResponse(valores, safe=False)


# V. Tabla: Ordenes, Obtener los ultimos registros de las necesidades en Tabla: plan_ordenes
def crear_planordenes(request):
    valores = {}
    valores["estado"] = False
    valores["modo"] = "Ejecutar Procedimiento Myqsl"
    valores["detalle"] = "abastece_planordenes"
    try:
        with connection.cursor() as cursor:
                cursor.callproc('abastece_planordenes')
                valores["estado"] = True
    except Exception as error:
        print("Error: ", type(error).__name__, "–", error)
        valores = "Error: " + str(error)
    return JsonResponse(valores, safe=False)

# V. Tabla: Ordenes, Obtener los ultimos registros de las necesidades en Tabla: plan_ordenes
def crear_pruebas(request):
    valores = {}
    valores["estado"] = False
    valores["modo"] = "Pruebas"
    valores["detalle"] = "Ordenes"
    try:
        reservas = pd.DataFrame(PlanReservas.objects.values())
        ordenes = pd.DataFrame(PlanAvisorden.objects.values())

        # Agrupar las tablas con la clave Orden de trabajo
        ordenreservas = reservas.merge(ordenes, how="left", on="orden")
       
        ordenes02 = pd.DataFrame(PlanOrdenes.objects.values())
        
        # Eliminar columnas que no se usan
        ordenreservas.drop(columns='id_y', inplace=True)        
        
        ordenes02.drop(columns='id', inplace=True)
        ordenes02.drop(columns='fechacarga', inplace=True)
        # ordenes02.drop(columns='orden', inplace=True)
        ordenes02.drop(columns='aviso', inplace=True)
        ordenes02.drop(columns='claot', inplace=True)
        # ordenes02.drop(columns='equipo', inplace=True)
        ordenes02.drop(columns='material', inplace=True)
        # ordenes02.drop(columns='felib', inplace=True)
        ordenes02.drop(columns='orden_texto', inplace=True)
        ordenes02.drop(columns='orden_estsis', inplace=True)
        # ordenes02.drop(columns='reservasolped', inplace=True)
        ordenes02.drop(columns='local', inplace=True)
        ordenes02.drop(columns='orden_revision', inplace=True)
        ordenes02.drop(columns='estatususuarioorden', inplace=True)
        ordenes02.drop(columns='orden_claact', inplace=True)
        ordenes02.drop(columns='centro', inplace=True)
        ordenes02.drop(columns='area_empr', inplace=True)
        ordenes02.drop(columns='costos_total_plan', inplace=True)
        ordenes02.drop(columns='costos_total_real', inplace=True)
        ordenes02.drop(columns='moneda', inplace=True)
        ordenes02.drop(columns='orden_prio', inplace=True)
        ordenes02.drop(columns='orden_prio_texto', inplace=True)
        ordenes02.drop(columns='estado_inst', inplace=True)
        ordenes02.drop(columns='ptotbjores_cod', inplace=True)
        ordenes02.drop(columns='gruplan', inplace=True)
        ordenes02.drop(columns='centro_planif', inplace=True)
        ordenes02.drop(columns='ubitec_deno', inplace=True)
        ordenes02.drop(columns='emplazamiento', inplace=True)
        ordenes02.drop(columns='emplcentro', inplace=True)
        
        ordenreservas = ordenreservas.merge(ordenes02, how="left", on="orden")        
        
        ordenreservas['felib'] = np.where( ordenreservas['felib_x'].isnull(), ordenreservas['felib_y']  , ordenreservas['felib_x'])
        ordenreservas['equipo'] = np.where( ordenreservas['equipo_x'].isnull(), ordenreservas['equipo_y']  , ordenreservas['equipo_x'])
        
        print(ordenreservas.loc[:,['felib_x','felib_y','felib', 'equipo_x','equipo_y', 'equipo']])
        
        valores["estado"] = True
        
    except Exception as error:
        print("Error: ", type(error).__name__, "–", error)
        valores = "Error: " + str(error)
    return JsonResponse(valores, safe=False)


# VI. Realizar el planeamiento en la Tabla: plan_ordenesreservas   
def crear_planabastecimiento(_request):
    valores = {}    
    valores["estado"] = False
    try:       
        reservas = pd.DataFrame(PlanReservas.objects.values())
        ordenes = pd.DataFrame(PlanAvisorden.objects.values())
        ordenes02 = pd.DataFrame(PlanOrdenes.objects.values())
        qreservas = len(reservas)
        qordenes = len(ordenes)
       
        # Agrupar las tablas con la clave Orden de trabajo
        ordenreservas = reservas.merge(ordenes, how="left", on="orden")
        qordenreservas = len(ordenreservas)       

        # Acortar para hacerlo mas rapido
        # ordenreservas = ordenreservas.sample(50)
                
        # Eliminar columnas que no se usan
        ordenreservas.drop(columns='id_y', inplace=True)
        ordenes02.drop(columns='id', inplace=True)
        ordenes02.drop(columns='fechacarga', inplace=True)
        # ordenes02.drop(columns='orden', inplace=True)
        ordenes02.drop(columns='aviso', inplace=True)
        # ordenes02.drop(columns='claot', inplace=True) pasar a Detalle 02
        # ordenes02.drop(columns='equipo', inplace=True)
        ordenes02.drop(columns='material', inplace=True)
        # ordenes02.drop(columns='felib', inplace=True)
        # ordenes02.drop(columns='orden_texto', inplace=True)
        # ordenes02.drop(columns='orden_estsis', inplace=True)
        # ordenes02.drop(columns='reservasolped', inplace=True)
        ordenes02.drop(columns='local', inplace=True)
        # ordenes02.drop(columns='orden_revision', inplace=True)
        # ordenes02.drop(columns='estatususuarioorden', inplace=True) pasar a Detalle 01
        ordenes02.drop(columns='orden_claact', inplace=True)
        ordenes02.drop(columns='centro', inplace=True)
        ordenes02.drop(columns='area_empr', inplace=True)
        ordenes02.drop(columns='costos_total_plan', inplace=True)
        ordenes02.drop(columns='costos_total_real', inplace=True)
        ordenes02.drop(columns='moneda', inplace=True)
        ordenes02.drop(columns='orden_prio', inplace=True)
        ordenes02.drop(columns='orden_prio_texto', inplace=True)
        ordenes02.drop(columns='estado_inst', inplace=True)
        ordenes02.drop(columns='ptotbjores_cod', inplace=True)
        ordenes02.drop(columns='gruplan', inplace=True)
        ordenes02.drop(columns='centro_planif', inplace=True)
        ordenes02.drop(columns='ubitec_deno', inplace=True)
        ordenes02.drop(columns='emplazamiento', inplace=True)
        ordenes02.drop(columns='emplcentro', inplace=True)

        # Agrupar con las tabla Ordenes
        ordenreservas = ordenreservas.merge(ordenes02, how="left", on="orden")        

        # Obtener los campos unificados de 'felib' y 'equipo'
        ordenreservas['felib'] = np.where( ordenreservas['felib_x'].isnull(), ordenreservas['felib_y']  , ordenreservas['felib_x'])
        ordenreservas['equipo'] = np.where( ordenreservas['equipo_x'].isnull(), ordenreservas['equipo_y']  , ordenreservas['equipo_x'])
        ordenreservas['orden_texto'] = np.where( ordenreservas['orden_texto_x'].isnull(), ordenreservas['orden_texto_y']  , ordenreservas['orden_texto_x'])
        ordenreservas['orden_revision'] = np.where( ordenreservas['orden_revision_x'].isnull(), ordenreservas['orden_revision_y']  , ordenreservas['orden_revision_x'])
        ordenreservas['estatususuarioorden'] = ordenreservas['estatususuarioorden_x']
        ordenreservas['detalle01'] = ordenreservas['estatususuarioorden_y']
        ordenreservas['detalle02'] = ordenreservas['claot']
        
        # Eliminar las columnas sobrantes de Ordenreservas
        ordenreservas.drop(columns='felib_x', inplace=True)
        ordenreservas.drop(columns='felib_y', inplace=True)
        ordenreservas.drop(columns='equipo_x', inplace=True)
        ordenreservas.drop(columns='equipo_y', inplace=True)
        ordenreservas.drop(columns='orden_texto_x', inplace=True)
        ordenreservas.drop(columns='orden_texto_y', inplace=True)
        ordenreservas.drop(columns='orden_revision_x', inplace=True)
        ordenreservas.drop(columns='orden_revision_y', inplace=True)
        
        # Agregar columnas faltantes
        ordenreservas['ate_accion'] = ""
        ordenreservas['ate_codigosap'] = ""
        ordenreservas['ate_cantidad'] = 0.01
        ordenreservas['ate_cantidad'] = 0.01
        ordenreservas['ate_UMB'] = ""
        ordenreservas['ate_orden'] = 999
        ordenreservas['ate_fecha'] = ""
        ordenreservas['valor_flota'] = 0.01

        # APLICAR FORMATOS
        # 1. Fechas
        ordenreservas['fechacarga_x'] = ordenreservas['fechacarga_x'].dt.strftime("%Y-%m-%d %H:%M:%S")
        ordenreservas['fechacarga_y'] = ordenreservas['fechacarga_y'].dt.strftime("%Y-%m-%d %H:%M:%S")
        ordenreservas['fechacarga_x'] = ordenreservas['fechacarga_x'].astype('object')
        ordenreservas['fechacarga_y'] = ordenreservas['fechacarga_y'].astype('object')
        # 2. Numeros decimales
        # ordenreservas['ctd_nec'] = ordenreservas['ctd_nec'].astype('float64')
        # ordenreservas['ctd_dif'] = ordenreservas['ctd_dif'].astype('float64')
        # ordenreservas['ctd_reduc'] = ordenreservas['ctd_reduc'].astype('float64')
        # ordenreservas['parada_dias'] = ordenreservas['parada_dias'].astype('float64')
        # ordenreservas['eqvaloradq_usd'] = ordenreservas['eqvaloradq_usd'].astype('float64')        
        # ordenreservas.style.format("{:.2f}")
        
        # 3. Cambiamos los valores NaN por 1 en el campo de valor del equipo
        ordenreservas['eqvaloradq_usd'] = ordenreservas['eqvaloradq_usd'].replace({np.nan: 1})
        
        # 4. Cambiamos los NaN por None que llegara a Mysql como NULL
        ordenreservas = ordenreservas.replace({np.nan: None})
        
        # REVISION DE TABLA FINAL
        # print(ordenreservas)
        # print(ordenreservas.columns.values)
        # print(ordenreservas.dtypes)

        # DETERMINAR ACCION de Abastecimiento
        # 1. Revisamos los Servicios
        ordenreservas.loc[ordenreservas['um_base'] == "ZZ", 'ate_accion'] = "SERVICIO"
        # 2. Revisamos las Reparaciones
        ordenreservas.loc[ordenreservas['lote'] == "REPARADO", 'ate_accion'] = "REPARADO"
        # 3. Revisamos la Mercaderia
        ordenreservas.loc[ordenreservas['ate_accion'] == "", 'ate_accion'] = "MERCADERIA"
        # 4. Anulamos los que no se deben atender: GARANTIA ubicado en el campo LOTE/Reservas Borradas/Reservas Atendidas o con Orden Cerrada campo salida_fin
        ordenreservas.loc[ordenreservas['salida_fin'] == "X" , 'ate_accion'] = "FIN"
        ordenreservas.loc[ordenreservas['reserva_pos_borrado'] == "X", 'ate_accion'] = "FIN"
        ordenreservas.loc[ordenreservas['lote'] == "GARANTIA" , 'ate_accion'] = "FIN"
        ordenreservas.loc[ordenreservas['reservasolped'] == "2" , 'ate_accion'] = "FIN"

        # DETERMINAR ORDEN del Abastecimento y las Ateciones
        # 1. Por semanas de Planificacion
        # ordenreservas.loc[ordenreservas['orden_revision_texto'] == "" , 'orden_revision_texto'] = "Programa Semanal por agendar"

        # 2. Secuencias de Ordenamiento
        
        # 2.1 Personas
        # Personas -> EPPs y Uniformes
        ordenreservas.loc[ordenreservas['orden'].str[0] == "P" , 'ate_orden'] = 100

        # 2.2 Equipos/Ventas

        # STC
        # ---
        
        # Equipos -> Ordenes de trabajo Libres o Aprovisionadas con Programa Semanal
        # OCO -> 4er Todas las Ordenes Liberadas o con Aprovisionamiento, con Numero de semana, de Campo
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') , 250, ordenreservas['ate_orden'])
        # INO -> 1er Orden Los Inoperativos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "I"), 210, ordenreservas['ate_orden'])
        # MAN -> 2er Orden Los Mantenimientos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "M"), 220, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Mantenimiento Preventivo') & (ordenreservas['orden_texto'].str[0]== "M"), 220, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Mantenimiento SSGG') & (ordenreservas['orden_texto'].str[0]== "M"), 220, ordenreservas['ate_orden'])
        # OCO -> 3er Orden Los Operativos con Observaciones
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "O"), 240, ordenreservas['ate_orden'])

        # Equipos -> Ordenes de trabajo Libres o Aprovisionadas sin Programa Semanal
        # OCO -> 4er Todas las Ordenes Liberadas o con Aprovisionamiento, con Numero de semana, de Campo
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') , 300, ordenreservas['ate_orden'])
        # INO -> 1er Orden Los Inoperativos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "I"), 260, ordenreservas['ate_orden'])
        # MAN -> 2er Orden Los Mantenimientos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "M"), 270, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Mantenimiento Preventivo') & (ordenreservas['orden_texto'].str[0]== "M"), 270, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Mantenimiento SSGG') & (ordenreservas['orden_texto'].str[0]== "M"), 270, ordenreservas['ate_orden'])
        # OCO -> 3er Orden Los Operativos con Observaciones
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "X" ) | ((ordenreservas['relevplnec'] == "X" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "O"), 290, ordenreservas['ate_orden'])

        # Equipos -> Ordenes de trabajo NO Libres o NO Aprovisionadas con Programa Semanal
        # OCO -> 4er Todas las Ordenes Liberadas o con Aprovisionamiento, con Numero de semana, de Campo
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') , 950, ordenreservas['ate_orden'])
        # INO -> 1er Orden Los Inoperativos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "I"), 910, ordenreservas['ate_orden'])
        # MAN -> 2er Orden Los Mantenimientos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "M"), 920, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Mantenimiento Preventivo') & (ordenreservas['orden_texto'].str[0]== "M"), 920, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Mantenimiento SSGG') & (ordenreservas['orden_texto'].str[0]== "M"), 920, ordenreservas['ate_orden'])
        # OCO -> 3er Orden Los Operativos con Observaciones
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "O"), 940, ordenreservas['ate_orden'])

        # Equipos -> Ordenes de trabajo NO Libres o NO Aprovisionadas sin Programa Semanal
        # OCO -> 4er Todas las Ordenes Liberadas o con Aprovisionamiento, con Numero de semana, de Campo
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') , 990, ordenreservas['ate_orden'])
        # INO -> 1er Orden Los Inoperativos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "I"), 960, ordenreservas['ate_orden'])
        # MAN -> 2er Orden Los Mantenimientos
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "M"), 970, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Mantenimiento Preventivo') & (ordenreservas['orden_texto'].str[0]== "M"), 970, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Mantenimiento SSGG') & (ordenreservas['orden_texto'].str[0]== "M"), 970, ordenreservas['ate_orden'])
        # OCO -> 3er Orden Los Operativos con Observaciones
        ordenreservas['ate_orden'] = np.where( ((ordenreservas['ot_liberado'] == "" ) & ((ordenreservas['relevplnec'] == "" ))) & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Campo') & (ordenreservas['orden_texto'].str[0]== "O"), 980, ordenreservas['ate_orden'])

        # Agrupar por Valor de Flota
        lista_criterio1 = list(ordenreservas["proyecto"])
        lista_criterio2 = list(ordenreservas["ate_orden"])
        valor_flota = [ordenreservas.loc[(ordenreservas['proyecto'] == lista_criterio1[i]) & (ordenreservas['ate_orden'] ==lista_criterio2[i]),"eqvaloradq_usd"].sum() for i in range(ordenreservas.shape[0])]
        # valor_flota.format("{:.2f}")
        valor_flota = pd.DataFrame(valor_flota)
        print(valor_flota)
        ordenreservas["valor_flota"] = valor_flota
        
        # STT
        # ---
        
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "")  & (ordenreservas['oden_clase_deno'] == 'Reparación Taller'), 999, ordenreservas['ate_orden'])
        # Equipos -> Ordenes de trabajo Libres con Programa Semanal
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Reparación"), 230, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Preparación"), 230, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Reparación venta"), 230, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Alistamiento"), 240, ordenreservas['ate_orden'])
        
        # Equipos -> Ordenes de trabajo Libres sin Programa Semanal
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Reparación"), 280, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Preparación"), 280, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Reparación venta"), 280, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "X")  & (~(ordenreservas['orden_revision'].str[0]== "C")) & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Alistamiento"), 290, ordenreservas['ate_orden'])

        # Equipos -> Ordenes de trabajo NO Libres
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Reparación"), 990, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Preparación"), 990, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Reparación venta"), 990, ordenreservas['ate_orden'])
        ordenreservas['ate_orden'] = np.where( (ordenreservas['ot_liberado'] == "")  & (ordenreservas['orden_revision'].str[0]== "C") & (ordenreservas['oden_clase_deno'] == 'Reparación Taller') & (ordenreservas['orden_claact_deno'] == "Alistamiento"), 990, ordenreservas['ate_orden'])

        # 2.3 Equipamiento y Otros

        # Reservas para Centro de Costos
        ordenreservas['ate_orden'] = np.where( (ordenreservas['orden'].str[0]== ""), 500, ordenreservas['ate_orden'])
        # Ordenes de Proyecto: 1 (113xxxx -> Proyectos de Mejora / 114xxxxx -> Compra de Activos / 18xxx -> Proyectos Campo) 
        ordenreservas.loc[ordenreservas['orden'].str[0] == "1" , 'ate_orden'] = 600
        # Ordenes de Proyecto: 2
        ordenreservas.loc[ordenreservas['orden'].str[0] == "2" , 'ate_orden'] = 620
        # Ordenes de Capacitacion: 7
        ordenreservas.loc[ordenreservas['orden'].str[0] == "7" , 'ate_orden'] = 640
        
        # Las reservas que no se vana utilizar (ate_accion = "FIN"), colocar 999
        ordenreservas.loc[ordenreservas['ate_accion'] == "FIN" , 'ate_orden'] = 999
        ordenreservas.loc[ordenreservas['ate_orden'] == 999 , 'ate_accion'] = "FIN"
        
        # DAR ORDEN AL DATAFRAME
        ordenreservas.sort_values(by = ['ate_orden', 'valor_flota','fe_nece', 'reserva', 'reservapos'], ascending = [True, False, True, True, True], na_position = 'last')

        # Reordenar columnas en Ordenreserva
        ordenreservas = ordenreservas.reindex([ 'id_x','fechacarga_y','orden','felib','aviso','empldeno','zona','equipo','eqdescrip','repercusion','cliente','proyecto','ave_ini_fecha','ave_fin_fecha','parada',
                                                'parada_dias','ubitec_deno','local','undneg','centro_deno','eq_est_usu_deno','flota_tipo','fe_despacho','eq_serie_motor','eq_serie_equipo','eq_est_ot_deno','clase','grupo_planif',
                                                'cliente_nro','proyecto_nro','supres_nombre','criticidad_deno','eqvaloradq_usd','repercusiondeno','oden_clase_deno','coti_esta_deno','avisodespacho','estatususuarioorden',
                                                'aviso_fecreado','orden_fe_fin_ext','orden_fe_ini_ext','fabricaequipo','orden_fecietec','orden_claact_deno','gruplan_deno','centro_y','eq_clase','orden_tipimput','orden_fecrea','orden_texto',
                                                'orden_prio','ot_abierto','ot_liberado','ot_cierrete','ot_cerrado','hruta_contador','hruta_grupo','aviso_prioridad_deno','aviso_clase_deno','orden_revision','orden_revision_texto','orden_causas_cod',
                                                'orden_causas','orden_causas_texto','cotizacion','pedido_venta','orden_pos_mtto','plan_mantenimiento','fechacarga_x','reserva','reservapos','material','materialdeno','ctd_nec','ctd_reduc',
                                                'ctd_dif','um_base','usuario','centro_x','almacen','lote','fe_nece','orden_op','dest_merc','imputacion','ce_coste','salida_fin','relevplnec','grafo','elem_pep','febase','reservaestatus','reservaimputacion',
                                                'indicador_dh','reserva_pos_borrado','reserva_mov_permit','ate_accion','ate_codigosap','ate_cantidad','ate_UMB','ate_orden','ate_fecha','valor_flota','reservasolped','detalle01','detalle02'], axis=1)
        
        
        # INICIO DE CARGAS A MYSQL
        # 0. Borar el contenido de la tabla
        
        with connection.cursor() as cursor01:
                cursor01.callproc('abastece_limpia_ordenreservas')
        
        # 1.Dividir el DataFrame en chunks de 1000 filas cada uno
        chunk_size = 100
        num_chunks = 0
        num_chunks = len(ordenreservas) // chunk_size + (1 if len(ordenreservas) % chunk_size else 0)
        chunks = [ordenreservas[i*chunk_size:(i+1)*chunk_size] for i in range(num_chunks)]
        # 2. Generar la consulta de ingreso
        mysqlplanordenreserva = """
                                INSERT INTO `uqmjvdmy_cgmrental`.`plan_ordenreserva`
                                (`id`,`fechacarga`,`orden`,`felib`,`aviso`,`empldeno`,`zona`,`equipo`,`eqdescrip`,`repercusion`,`cliente`,`proyecto`,`ave_ini_fecha`,`ave_fin_fecha`,`parada`,`parada_dias`,`ubitec_deno`,
                                `local`,`undneg`,`centro_deno`,`eq_est_usu_deno`,`flota_tipo`,`fe_despacho`,`eq_serie_motor`,`eq_serie_equipo`,`eq_est_ot_deno`,`clase`,`grupo_planif`,`cliente_nro`,`proyecto_nro`,`supres_nombre`,
                                `criticidad_deno`,`eqvaloradq_usd`,`repercusiondeno`,`oden_clase_deno`,`coti_esta_deno`,`avisodespacho`,`estatususuarioorden`,`aviso_fecreado`,`orden_fe_fin_ext`,`orden_fe_ini_ext`,`fabricaequipo`,
                                `orden_fecietec`,`orden_claact_deno`,`gruplan_deno`,`centro`,`eq_clase`,`orden_tipimput`,`orden_fecrea`,`orden_texto`,`orden_prio`,`ot_abierto`,`ot_liberado`,`ot_cierrete`,`ot_cerrado`,`hruta_contador`,
                                `hruta_grupo`,`aviso_prioridad_deno`,`aviso_clase_deno`,`orden_revision`,`orden_revision_texto`,`orden_causas_cod`,`orden_causas`,`orden_causas_texto`,`cotizacion`,`pedido_venta`,`orden_pos_mtto`,`plan_mantenimiento`,
                                `reserva_fechacarga`,`reserva`,`reservapos`,`material`,`materialdeno`,`ctd_nec`,`ctd_reduc`,`ctd_dif`,`um_base`,`usuario`,`reserva_centro`,`reserva_almacen`,`lote`,`fe_nece`,`orden_op`,`dest_merc`,`imputacion`,`ce_coste`,
                                `salida_fin`,`relevplnec`,`grafo`,`elem_pep`,`febase`,`reservaestatus`,`reservaimputacion`,`indicador_dh`,`reserva_pos_borrado`,`reserva_mov_permit`,`ate_accion`,`ate_codigosap`,`ate_cantidad`,`ate_UMB`,`ate_orden`,
                                `ate_fecha`,`valor_flota`,`reservasolped`,`detalle01`,`detalle02`)
                                VALUES
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                """
        # 3. Hacer la carga de las partes
        total = num_chunks
        avance = 0
        for chunk in chunks:
            avance = avance + 1
            # print(valor_flota)
            print(avance)
            # print(chunk)            
            print("El avance es : ",avance,"/",total)
            records = [tuple(x) for x in chunk.to_numpy()]
            with connection.cursor() as cursor:
                cursor.executemany(mysqlplanordenreserva, records)
        # FIN DE CARGAS        
              
        # DATOS DE SALIDA
        # 1. Convertir la DATA a JSON        
        # lista = ordenreservas.to_numpy().tolist()
        # valores["data"]={'data':lista} 
        # 2. Mostrar resultados en registros en JSON
        
        valores["estado"] = True
        valores["reservas"] = str(qreservas)
        valores["ordenes"] = str(qordenes)
        valores["ordenreservas"] = str(qordenreservas)
        valores["bloque"] = str(chunk_size) + " Registros"
        valores["nro_bloques"] = str(num_chunks)
        valores["avance"] = str(avance) + "/" + str(num_chunks)
         
    except Exception as error:
        print("Error: ", type(error).__name__, "–", error)
        valores["error"] = "Error: " + str(error)
        valores["estado"] = False
        
    return JsonResponse(valores, safe=False)
    # return HttpResponse(valores)
