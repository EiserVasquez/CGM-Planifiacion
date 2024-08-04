from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.db import connection
import pandas as pd
import seaborn as sns
import numpy as np
# import seaborn as sns

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

def limpiar_tablasplan(request):
    borrado = False
    try:
        with connection.cursor() as cursor:
            cursor.callproc('limpieza_tablas_plan')
            borrado = True
    except Exception as error:
        borrado = False
    return borrado   


def limpiar_planordenreserva(request):
    borrado = False
    with connection.cursor() as cursor:
        try:
            cursor.callproc('abastece_limpia_ordenreservas')
            borrado = True
        except Exception as error:
            borrado = False
    return borrado

def crear_planavisorden(request):
    creado = False
    try:
        with connection.cursor() as cursor:
                cursor.callproc('abastece_planavisorden')
                creado = True
    except Exception as error:
        creado = False                
    return creado

def crear_planreservas(request):
    creado = False
    try:
        with connection.cursor() as cursor:
                cursor.callproc('abastece_planreservas')
                creado = True
    except Exception as error:
        creado = False                
    return creado
    
def crear_previos(_request):
    creado = False
    try:       
        reservas = pd.DataFrame(PlanReservas.objects.values())
        ordenes = pd.DataFrame(PlanAvisorden.objects.values())
        qreservas = len(reservas)
        qordenes = len(ordenes)
       
        # Agrupar las tablas con la clave Orden de trabajo
        ordenreservas = reservas.merge(ordenes, how="left", on="orden")
        qordenreservas = len(ordenreservas)       

        
        # Acortar para hacerlo mas rapido
        # ordenreservas = ordenreservas.sample(50)
                
        # Eliminar columnas que no se usan
        ordenreservas.drop(['id_y'],axis=1)

        # Agregar columnas faltantes
        ordenreservas['ate_accion'] = ""
        ordenreservas['ate_codigosap'] = ""
        ordenreservas['ate_cantidad'] = 0
        ordenreservas['ate_UMB'] = ""
        ordenreservas['ate_orden'] = 0
        ordenreservas['ate_fecha'] = ""

        # Reordenar columnas en Ordenreserva
        ordenreservas = ordenreservas.reindex([ 'id_x','fechacarga_y','orden','felib','aviso','empldeno','zona','equipo','eqdescrip','repercusion','cliente','proyecto','ave_ini_fecha','ave_fin_fecha','parada',
                                                'parada_dias','ubitec_deno','local','undneg','centro_deno','eq_est_usu_deno','flota_tipo','fe_despacho','eq_serie_motor','eq_serie_equipo','eq_est_ot_deno','clase','grupo_planif',
                                                'cliente_nro','proyecto_nro','supres_nombre','criticidad_deno','eqvaloradq_usd','repercusiondeno','oden_clase_deno','coti_esta_deno','avisodespacho','estatususuarioorden',
                                                'aviso_fecreado','orden_fe_fin_ext','orden_fe_ini_ext','fabricaequipo','orden_fecietec','orden_claact_deno','gruplan_deno','centro_y','eq_clase','orden_tipimput','orden_fecrea','orden_texto',
                                                'orden_prio','ot_abierto','ot_liberado','ot_cierrete','ot_cerrado','hruta_contador','hruta_grupo','aviso_prioridad_deno','aviso_clase_deno','orden_revision','orden_revision_texto','orden_causas_cod',
                                                'orden_causas','orden_causas_texto','cotizacion','pedido_venta','orden_pos_mtto','plan_mantenimiento','fechacarga_x','reserva','reservapos','material','materialdeno','ctd_nec','ctd_reduc',
                                                'ctd_dif','um_base','usuario','centro_x','almacen','lote','fe_nece','orden_op','imputacion','ce_coste','salida_fin','relevplnec','grafo','elem_pep','febase','reservaestatus','reservaimputacion',
                                                'indicador_dh','reserva_pos_borrado','reserva_mov_permit','ate_accion','ate_codigosap','ate_cantidad','ate_UMB','ate_orden','ate_fecha'], axis=1)
        
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
        # 3. Cambiamos los NaN por None que llegara a Mysql como NULL
        ordenreservas = ordenreservas.replace({np.nan: None})
        
        # REVISION DE TABLA FINAL
        # print(ordenreservas)
        # print(ordenreservas.columns.values)
        # print(ordenreservas.dtypes)
        
        
        # INICIO DE CARGAS A MYSQL
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
                                `reserva_fechacarga`,`reserva`,`reservapos`,`material`,`materialdeno`,`ctd_nec`,`ctd_reduc`,`ctd_dif`,`um_base`,`usuario`,`reserva_centro`,`reserva_almacen`,`lote`,`fe_nece`,`orden_op`,`imputacion`,`ce_coste`,
                                `salida_fin`,`relevplnec`,`grafo`,`elem_pep`,`febase`,`reservaestatus`,`reservaimputacion`,`indicador_dh`,`reserva_pos_borrado`,`reserva_mov_permit`,`ate_accion`,`ate_codigosap`,`ate_cantidad`,`ate_UMB`,`ate_orden`,`ate_fecha`)
                                VALUES
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                """
        # 3. Hacer la carga de las partes
        total = num_chunks
        avance = 0
        for chunk in chunks:
            print(chunk)
            avance = avance + 1
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
        valores = {}
        valores["reservas"] = str(qreservas)
        valores["ordenes"] = str(qordenes)
        valores["ordenreservas"] = str(qordenreservas)
        valores["bloques"] = str(num_chunks)
        valores["avance"] = str(avance) + "/" + str(num_chunks)
        
        creado = True
         
    except Exception as error:
        creado = False
        print("Error: ", type(error).__name__, "–", error)
        valores = "Error: " + str(error)
        creado = False
        
    return JsonResponse(valores, safe=False)
    # return HttpResponse(valores)
