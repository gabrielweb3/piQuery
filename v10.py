#librerias tkinter
import tkinter
from tkinter import *
from tkinter import ttk

#librerias PI
import sys  
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')  
import clr
from clr import AddReference
clr.AddReference('OSIsoft.AFSDK')  
import os
from os import scandir
from os import remove

from OSIsoft.AF import *  
from OSIsoft.AF.PI import * 
from OSIsoft.AF.Search import *   
from OSIsoft.AF.Asset import *  
from OSIsoft.AF.Data import *  
from OSIsoft.AF.Time import *  
from OSIsoft.AF.UnitsOfMeasure import *

#otras librerias 
import time
import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
# from datetime import datetime
#from matplotlib.dates import bytespdate2num
# import matplotlib.pyplot as plt
from matplotlib.dates import date2num
# from matplotlib import dates as mpl_dates
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import math
import difflib as dlb
import warnings

#FUNCIONES
################################################################
#FUNCIONES PARA RECORRER PISYSTEM Y SELECCIONAR OBJETOS A TRABAJAR

#CONEXION A PIDATACOLLECTIVE
def connect_to_PISystem(serverName):  
    piSystems = PISystems()  
    global piSystem  
    piSystem = piSystems[serverName]  
    piSystem.Connect()
    
def connect_to_Server(serverName):  
    piServers = PIServers()  
    global piServer  
    piServer = piServers[serverName]  
    piServer.Connect(False)
        
def obtener_elementos(objeto):    
    if isinstance(objeto, PISystem):
         elementos_encontrados=objeto.Databases
    else:
         elementos_encontrados=objeto.Elements    
    return elementos_encontrados

def obtener_atributos(objeto):
    if isinstance(objeto, AFElement):
        atributos_encontrados=objeto.Attributes
    else:
        atributos_encontrados=[]
    return atributos_encontrados

#transformar coleccion de elementos, debido a que los elementos del tipo AFDatabases, AFElements y AFAttributes
#no son indexables, se crea un funcion que toma esos elementos y los duplica en un array comun (objetos_encontrados),
#que puede ser utilizado por otras funciones sin problemas mostrar_ruta.set(atributos_encontrados.GetPath())
def transformar_coleccion_AF(coleccion):
    objetos_encontrados=[]    
    for elemento in coleccion:            
        objetos_encontrados.append(elemento) 
    return objetos_encontrados
    
#esta funcion borra todos los elementos de la lista actual antes de introducir elementos nuevos
def borrar_listado(listado):
    listado.delete(0,END)

#esta funcion muestra el numero de item actualmente seleccionado, a menos que no haya nada seleccionado
def mostrar_item():
    try:
        item = listbox.curselection()
        # print(int(item[0]))
    except:
        pass
    
#esta funcion actualiza la lista de elementos que se esta usando, primero llamando a la funcion borrar listado
#luego para cada elemento consulta si es el actualmente seleccionado, en caso de que si, inserta el elemento al final
#y obtiene la ruta del mismo, en caso contrario obtiene unicamente el nombre, por lo tanto el elemento no se podra llamar
def actualizar_listado(elementos, listado):
    borrar_listado(listado)
    for item in elementos:        
        if elementos==atributos_seleccionados:            
            listado.insert(END, item.GetPath())
        else:
            listado.insert(END, item.Name)

#esta funcion define la utilidad del boton desplegar, utilizando el listado actual seleccionado y la lista de atributos actuales
#en el try lo que hace es definir item como el el elemento actual seleccionado, ese primer comando esta puesto en
#primer lugar ya que es la unica accion que podria fallar, ya que si no se tiene seleccionado ningun elemento, se sale
#del try y sale de la funcion. En caso de que haya un elemento selecionado toma el primer elemento del listado
#y declara que el objeto seleccionado es el primero del listado acutal, luego agrega la ruta del objeto seleccionado al array de ruta
#luego obtiene los elementos hijos del elemento seleccionado, los transforma en un array indexable, actualiza el listado
#luego obtiene los atributos del objeto, los transforma en un array indexable, y vuelve a actualizar el listado, pero esta vez de atributos
#del elemento, por lo tanto en el segundo listbox apareceran los atributos del elemento seleccionado en el primer listbox
def avanzar():
    global listado_actual
    global listado_atributos_actual
    try:
        item = lista_elementos.curselection()
        num_item=int(item[0])
        objeto_seleccionado = listado_actual[num_item]
        ruta.append(objeto_seleccionado)
        coleccion_AF = obtener_elementos(objeto_seleccionado)
        listado_actual = transformar_coleccion_AF(coleccion_AF)
        actualizar_listado(listado_actual, lista_elementos)
        atributos_AF = obtener_atributos(objeto_seleccionado)
        listado_atributos_actual = transformar_coleccion_AF(atributos_AF)
        actualizar_listado(listado_atributos_actual, lista_atributos) 
        mostrar_ruta.set(objeto_seleccionado.GetPath())
    except:
        pass
    
#tomo el listado actual, el atributo actual y el objeto seleccionado, si la ruta esta vacia paso a la siguiente funcion
        #sino elimino la ultima entrada de la ruta, y vuelvo a checkear si la ruta esta vacia, sino lo esta leo la ruta
        #desde su ultimo elemento y lo selecciono como elemento actual, si la ruta esta vacia significa que no hay
        #elementos seleccionados por lo tanto el elemento sera piSystem, por lo tanto me encotrare en la primera
        #listbox, acutializo el listado y muestro el elemento actual que en caso de que la ruta este vacia sera piSystem

def retroceder():

    global listado_actual
    global listado_atributos_actual
    global objeto_seleccionado
    if len(ruta) == 0:
        pass
    else:
        ruta.pop()
        if len(ruta)>0:
            objeto_seleccionado = ruta[-1]
            coleccion_AF = obtener_elementos(objeto_seleccionado)
            listado_actual = transformar_coleccion_AF(coleccion_AF)
            atributos_AF = obtener_atributos(objeto_seleccionado)
            listado_atributos_actual = transformar_coleccion_AF(atributos_AF)
            mostrar_ruta.set(objeto_seleccionado.GetPath())
        else:
            listado_actual = []
            listado_actual.append(piSystem)
            listado_atributos_actual = []

        actualizar_listado(listado_actual, lista_elementos)
        actualizar_listado(listado_atributos_actual, lista_atributos)
        
#defino el doble click como avanzar, significa que al hacer doble click en el elemento, cumplira la misma funcion
#que apretar el boton desplegar
def avanzar_dblclick(event):
    avanzar()

#esta funcion toma los atributos selecciondos y el listado de atributos actual, toma el atributo actual y lo agrega a la lista de elementos seleccionados (variables seleccionadas)
def agregar_seleccion():

    global listado_atributos_actual
    global atributos_seleccionados
    try:   
        item = lista_atributos.curselection()
        num_item = int(item[0])    
        atributo_seleccionado = listado_atributos_actual[num_item]
        atributos_seleccionados.append(atributo_seleccionado)
        actualizar_listado(atributos_seleccionados, lista_seleccionados)
        lista_seleccionados.yview_moveto(1)        
        
    except:
        pass

#en caso de seleccionar el atributo con doble click en lugar de apretar el boton agregar
def agregar_seleccion_dblclick(event):
    agregar_seleccion()

#elimina el elemento seleccionado de la lista de elementos seleccionados
def quitar_seleccion():    
    global listado_atributos_actual
    global atributos_seleccionados
    try:   
        item = lista_seleccionados.curselection()
        num_item = int(item[0])    
        atributos_seleccionados.pop(num_item)        
        actualizar_listado(atributos_seleccionados, lista_seleccionados)
    except:
        pass

#mostrar variables individualmete en un listbox
def lista_variables():
    global atributos_seleccionados, ag_actual, aerogens
    if len(ruta)>=4:
        ag_actual.set(ruta[3])
        aerogens.append(ruta[3])
    else:
        ag_actual.set(" - ")
        # str_aeros.set(" - ")
    for var in range(0,len(atributos_seleccionados)):
        #variables.append(atributos_seleccionados[aux])
        lista_var_selected.insert(END,atributos_seleccionados[var])
    # print(atributos_seleccionados)

#mostrar listado de aerogeneradores en un listbox
def lista_ags():
    global ruta
    aeros = obtener_elementos(ruta[2])
    listado_ags = transformar_coleccion_AF(aeros)
    for var in range(0,len(listado_ags)):
        lista_ag_list.insert(END, listado_ags[var])
        
#agregar ag a lista de seleccionados
def agregar_ag():
    global ruta, aerogens
    item = lista_ag_list.curselection()
    aeros = obtener_elementos(ruta[2])
    listado_ags = transformar_coleccion_AF(aeros)
    lista_ag_sel.insert(END, listado_ags[int(item[0])])
    aerogens.append(listado_ags[int(item[0])])
    
#agregar ag doble click
def agregar_ag_dblclick(event):
    agregar_ag()

#quitar ag de la lista de seleccionados
def quitar_ag():
    global aerogens
    item = lista_ag_sel.curselection()
    ind_item = item[0]
    lista_ag_sel.delete(ind_item)
    aerogens.pop(lista_ag_sel[ind_item])
    # actualizar_listado(elementos, aerogens)
    
#agregar todos los ags a la lista de seleccionados
def agregar_todos():
    global ruta
    aeros = obtener_elementos(ruta[2])
    listado_ags = transformar_coleccion_AF(aeros)
    for var in range(0,len(listado_ags)):
        lista_ag_sel.insert(END, listado_ags[var])
        aerogens.append(listado_ags[var])


#CONSULTA DE DATOS
#esta funcion se encarga de conectar con el servidor y traer todos los datos
#solicitados entre las fechas que se le diga
def cargarDatos():      
    from tqdm import tqdm
    global estado_text
    estado_txt.set("Cargando datos...")
    #Periodo  
    fecha_inicio = fecha_ini_var.get()
    fecha_fin = fecha_fin_var.get()
    lista_ags()
    
    #Tags
    signals = atributos_seleccionados
    senal = 0
    
    #Se definen variables necesarias para la consulta
    #Variable del tipo AFtimeRange con los valores de inicio y fin del periodo
    timerange = AFTimeRange(fecha_inicio, fecha_fin)

    #Genero los atributos para consulta
    global atributos_PI
    atributos_PI = []

    #Agrego los AFData correspondientes a los nombres de los Tags
    for senal in signals:    #☻☻☻☻☻☻☻☻
        atributos_PI.append(senal.PIPoint)        
        # atributos_PI.append(PIPoint.FindPIPoint(piServer, senal))
        # atributos_PI.append(senal.Data)
        # print(type(atributos_PI[0]),',',type(atributos_seleccionados[0]))
        
    #Genero las fechas ordenadas
    fecha_inicio_time=datetime.strptime(fecha_inicio,'%d/%m/%Y %H:%M')
    fecha_inicio_num=date2num(fecha_inicio_time)
    fecha_fin_time=datetime.strptime(fecha_fin,'%d/%m/%Y %H:%M')
    fecha_fin_num=date2num(fecha_fin_time)
    
    rango_fechas=pd.date_range(start=fecha_inicio_time, end=fecha_fin_time, freq="10min")
    indice_fechas=range(0,len(rango_fechas))
    
    #Genero DataFrame para guardar los datos consultado
    global df
    df=pd.DataFrame({"fecha":rango_fechas},index=indice_fechas)
    
    #Consulta de datos
    #Se consultan los datos para cada elemento de atributos_PI
    for consulta in tqdm(range(0,len(atributos_PI))):
        atributos_seleccionados[consulta] = atributos_PI[consulta].Name     
        nombre_atributo = atributos_PI[consulta].Name
        
        
        
        #Genero tres arrays vacíos para guardar los datos conultados
        fecha=[]
        datos=[]
        indice=[]

        #Variable para verificar ausencia de fechas repetidas
        fecha_anterior=datetime(1990,10,6,1,50)
    
        #Defino un DataFrame auxiliar para guardar los datos de un elemento
        df_aux=pd.DataFrame()
        
        resultado = atributos_PI[consulta].RecordedValues(timerange, AFBoundaryType.Inside, "", False)
    
        #Recorro todos los elementos del resulado de la consulta para...
        #...agregar los datos en los vectores correspondientes
        for event in resultado:

            #Solo agrego datos que conicidan con diezminutales
            if (event.Timestamp.LocalTime.Minute%10==0)and(event.Timestamp.LocalTime.Second==0):
            
                #Convierto al tipo datetime
                fecha_aux=datetime(event.Timestamp.LocalTime.Year,
                               event.Timestamp.LocalTime.Month,
                               event.Timestamp.LocalTime.Day,
                               event.Timestamp.LocalTime.Hour,
                               event.Timestamp.LocalTime.Minute)
            
                if fecha_aux!=fecha_anterior:
                
                    #Agrego fecha al vector
                    fecha.append(fecha_aux)

                    #Agrego dato al vector
                    datos.append(event.Value)
                    #Agrego su indice relativo a la fecha de inicio
                    indice.append(round((date2num(fecha_aux)*6*24)-(fecha_inicio_num*6*24)))
                    fecha_anterior=fecha_aux        
               
        nombre_columna2=nombre_atributo
        df_aux1=pd.DataFrame({nombre_columna2:datos},index=indice)
        df=pd.concat([df,df_aux1], axis=1, sort=False)
        
        #convertir dataframe a valores numericos
        #cuando el contenido no es numerico pone un NaN en su lugar
        df_2 = df.apply(pd.to_numeric,errors='ignore')
        
        #cuando hago esta conversion tambien convierte el vector de fechas a numerico
        #por lo tanto tengo que volver el vector de fechas a su estado original
        df_2['fecha'] = df['fecha']
        
        #luego de que df_2 queda con el la columna de fechas correcta, lo vuelvo a convertir en df
        df = df_2
        
        # filtrar nan
        df = df.fillna("")
        
        #cargar y actualizar barra de carga
        barra1['value']+=100/len(atributos_PI)
        ventana.update_idletasks()
       
        # funcion para eliminar columnas repetidas 
        # eliminar_columnas_repetidas(df)
        
    
    # exporto datos
    df.to_csv(str(ruta[1])+'_datos_crudos.csv')
    
    estado_txt.set(time.strftime("%H:%M - ") + "Se cargan los datos satisfactoriamente")
    refresh()
    #habilito botones inicialmente deshabilitados 
    btn_crear_atributos.config(state = NORMAL)
    
    lista_variables()    
    refresh() #actualiza variables en ventana de filtros    
    lista_ags()
                               
#EXPORTAR DATOS A CSV
#esta funcion se encarga de escribir los datos almacenados en el dataframe df
#y exportarlos a un archivo csv
def exportarDatos():
    df.to_csv(str(ruta[1])+'_datos_exportados.csv')
    global estado_txt
    estado_txt.set(time.strftime("%H:%M - ") + "Se exportan los datos satisfactoriamente")
    #df = []

#funcion para crear, para cada aerogenerador seleccionado, la cantidad de atributos igual...
#...a la seleccionada para el ag original
def crear_atributos_varios_ags():
    global atributos_PI, aerogens, atributos_finales
    
    #variable para tratar atributo individual
    atributo_actual = ''
    
    #convertir elementos de aerogens, tipo AFElements, a tipo string
    strings_aeros = []
    for aerogen in aerogens:
        strings_aeros.append(str(aerogen))
    
    #variables donde se almacenaran todas los atributos actuales
    atributos_finales = []
    
    #ahora trato cada atributo individualmente para cambiar el numero de AG
    for atributos in range(0,len(atributos_seleccionados)):
        #print(atributos_finales[atributos])
        atributo_actual = atributos_PI[atributos]
        #vector para almacenar el string separado letra por letra
        string_atributo_desarmado = []
        # agrego todos los atributos seleccionados anteriorment
        # atributos_finales.append(atributos_seleccionados[atributos])
        #separo cada letra del string de los aeros
        for ag in range(0,len(strings_aeros)):
            string_atributo_desarmado.append(list(str(atributo_actual)))
            
        #ahora separo los strings de cada ag desarmado
        string_ag_desarmado = []
        for ag in range(0,len(strings_aeros)):
            string_ag_desarmado.append(list(strings_aeros[ag]))
            
            #selecciono posicion especifica del string de atributos y lo cambio
            #por las posiciones del vector de ag donde se encuentra el numero de ag
            string_atributo_desarmado[ag][10] = string_ag_desarmado[ag][2]
            string_atributo_desarmado[ag][11] = string_ag_desarmado[ag][3]
            
            #armo nuevamente el vector de los strings con los atributos con los
            #numeros de ag cambiados
            atributos_finales.append(''.join(string_atributo_desarmado[ag]))
            
    for i in range(0,len(atributos_finales)):
        print(atributos_finales[i])
        
    global estado_txt
    # cargar_datos_ags()
    return atributos_finales
    
 ############### crea una sola funcion de carga ###### MONO! ########   
        
#cargar variables seleccionadas para aerogeneradores seleccionados
def cargar_datos_ags():     
    global aerogens, atributos_finales, atributos_seleccionados, estado_txt
    # lista_variables() 
    barra1.stop()
    estado_txt.set("Cargando datos...")
    # comparar atributos finales y atributos seleccionados para ver cual 
    # vector usar, si no se cargan variables de mas de un aerogenerador, 
    # se utilizara la variable atributos_seleccionados, de lo contrario se utiliza atributos_finales
    
    crear_atributos_varios_ags()
    
    from tqdm import tqdm # libreria de barra de progreso
    
    for ag in tqdm(range(0,len(aerogens))):
        #Periodo
        fecha_inicio = fecha_ini_var.get()
        fecha_fin = fecha_fin_var.get()
        
        #Tags
        print(type(atributos_finales[0]))
        signals = atributos_finales
        # signals = atributos_seleccionados
         
        #Se definen variables necesarias para la consulta
        #Variable del tipo AFtimeRange con los valores de inicio y fin del periodo
        timerange = AFTimeRange(fecha_inicio, fecha_fin)
    
        #Genero los atributos para consulta
        global atributos_PI
        atributos_PI = []
        
        #cargar y actualizar barra de carga
        # barra1['value']+=100/(len(atributos_seleccionados))
        # ventana.update_idletasks()
        
        #Agrego los AFData correspondientes a los nombres de los Tags
        for senal in signals:    
            atributos_PI.append(PIPoint.FindPIPoint(piServer, senal))
            # atributos_PI.append(senal.PIPoint) 
            # atributos_PI.append(senal.Data)
            
        #Genero las fechas ordenadas
        fecha_inicio_time=datetime.strptime(fecha_inicio,'%d/%m/%Y %H:%M')
        fecha_inicio_num=date2num(fecha_inicio_time)
        fecha_fin_time=datetime.strptime(fecha_fin,'%d/%m/%Y %H:%M')
        fecha_fin_num=date2num(fecha_fin_time)
        
        rango_fechas=pd.date_range(start=fecha_inicio_time, end=fecha_fin_time, freq="10min")
        indice_fechas=range(0,len(rango_fechas))
    
        #Genero DataFrame para guardar los datos consultado
        global df
        df=pd.DataFrame({"fecha":rango_fechas},index=indice_fechas)
        
        #Consulta de datos
        #Se consultan los datos para cada elemento de atributos_PI
        # for consulta in atributos_PI:
        for consulta in range(0,len(atributos_PI)):
            #Guardo el nombre del elemento que estoy consultando
            nombre_atributo = atributos_PI[consulta].Name
            
            #Genero tres arrays vacíos para guardar los datos conultados
            fecha=[]
            datos=[]
            indice=[]
    
            #Variable para verificar ausencia de fechas repetidas
            fecha_anterior=datetime(1990,10,6,1,50)
        
            #Defino un DataFrame auxiliar para guardar los datos de un elemento
            df_aux=pd.DataFrame()
    
            #La función RecordedValues me devuelve una colección de objetos que contiene todos los datos guardados en el periodo timerange del...
            #...elemento que estoy consultando
            resultado = atributos_PI[consulta].RecordedValues(timerange, AFBoundaryType.Inside, "", False)
    
            #Recorro todos los elementos del resulado de la consulta para...
            #...agregar los datos en los vectores correspondientes
            for event in resultado:
    
                #Solo agrego datos que conicidan con diezminutales
                if event.Timestamp.LocalTime.Minute%10==0:  
                
                    #Convierto al tipo datetime
                    fecha_aux=datetime(event.Timestamp.LocalTime.Year,
                                   event.Timestamp.LocalTime.Month,
                                   event.Timestamp.LocalTime.Day,
                                   event.Timestamp.LocalTime.Hour,
                                   event.Timestamp.LocalTime.Minute)
                
                    if fecha_aux!=fecha_anterior:
                    
                        #Agrego fecha al vector
                        fecha.append(fecha_aux)
    
                        #Agrego dato al vector
                        datos.append(event.Value)
                        #Agrego su indice relativo a la fecha de inicio
                        indice.append(round((date2num(fecha_aux)*6*24)-(fecha_inicio_num*6*24)))
                        fecha_anterior=fecha_aux
                
            nombre_columna2 = nombre_atributo
            df_aux1=pd.DataFrame({nombre_columna2:datos},index=indice)
            df=pd.concat([df,df_aux1], axis=1, sort=False)
            #convertir dataframe a valores numericos
            #cuando el contenido no es numeri¸co pone un NaN en su lugar
            df_2 = df.apply(pd.to_numeric,errors='coerce')
            #cuando hago esta conversion tambien convierte el vector de fechas a numerico
            #por lo tanto tengo que volver el vector de fechas a su estado original
            df_2['fecha'] = df['fecha']
            
            #luego de que df_2 queda con el la columna de fechas correcta, lo vuelvo a convertir en df
            df = df_2
            # filtrar nan
            df = df.fillna("")
        
        barra1['value'] += 100/len(aerogens)
        ventana.update_idletasks()
        
        # funcion para eliminar columnas repetidas 
        # eliminar_columnas_repetidas(datos)
            
    # exporto datos
    df.to_csv(str(ruta[1])+'_datos_crudos.csv')
    
    estado_txt.set(time.strftime("%H:%M - ") + "Se cargan los datos para todos los AGs satisfactoriamente")
    refresh()
    #habilito botones inicialmente deshabilitados 
    btn_crear_atributos.config(state = NORMAL)
    lista_variables()    
    refresh() #actualiza variables en ventana de filtros    
    lista_ags()
 
# funcion para tomar todos los filtros seleccionados en la interfaz y aplicarlos
# en el dataframe principal
def aplicar_filtros():
    # print('aplicando filtros...')
    global datos, vector_filtros, pendientes, estado_txt
    
    estado_txt.set('Aplicando filtros...')
    
    # elimino nan de df.datos
    datos = datos.fillna('')
    
    #limpiar barra de carga
    barra1.stop()

    start_time = time.time() #cuanto tiempo
    
    # filtrar_todos()
    #separo vector de fechas 
    date = pd.DataFrame(datos['fecha'])
    
    #vector para almacenar variables de los comboboxes "Variable Principal"
    main_variables = []
    #vector para almacenar señales de los entrys "Señal"
    replace_value = []
    #vector para almacenar los valores de los entrys del filtro de valores consecutivos
    consecutives = []
    #vector para almacenar los valores de los entrys del filtro de pendiente consecutivos
    pendientes = []
    #vector para almacenar variables de los comboboxes "Variable secundaroa"
    second_variables = []
    #vector para almacenar variables de los comboboxes "comparadores"
    comparadores = []
    #vector para almacenar variables de los entrys "valores de comparacion"
    valores_comparadores = []
    #vector para almacenar variables de los comboboxs de accion a realizar
    acciones = []
    
    #identificar los valores ingresados en la interfaz gráfica   
    for idx in range(0,len(combo)):       
        if combo[idx] != '0':
            main_variables.append(combo[idx].get()); 
        else: 
            main_variables[idx] = combo[idx].get()        
        
        if replace[idx] != '0':
            replace_value.append(replace[idx].get()); 
        else:
            replace_value[idx] = replace[idx].get()            
        
        if consecutivo_[idx] != '0':
            consecutives.append(consecutivo_[idx].get())
        else: 
            consecutives[idx] = consecutivo_[idx].get()           
        
        if pendiente_[idx] != '0':
            pendientes.append(pendiente_[idx].get())
        else: 
            pendientes[idx] = pendiente_[idx].get()       
        
        if combo2[idx] != '0':
            second_variables.append(combo2[idx].get()); 
        else: 
            second_variables[idx] = combo2[idx].get()       
        
        if comparador[idx] != '0':
            comparadores.append(comparador[idx].get())
        else: 
            comparadores[idx] = comparador[idx].get()       
        
        if compare_value[idx] != '0':
            valores_comparadores.append(compare_value[idx].get())
        else: 
            valores_comparadores[idx] = compare_value[idx].get()       
        
        if accion_[idx] != '0':
            acciones.append(accion_[idx].get())
        else: 
            acciones[idx] = accion_[idx].get()
    
    #creo variables para eliminar los espacios no seleccionados
    variables_principales = []
    variables_secundarias = []
    variables_reemplazo = []
    variables_consecutivo = []
    variables_pendientes = []
    variables_comparadores = []
    variables_comparacion = []
    variables_accion = []
    filtros_aplicados = []
    
    # cargar filtros aplicados para cada variable
    for i in range(0,len(acciones)): #creo posiciones en vector de filtros_aplicados
       filtros_aplicados.append([]) 
    # contador_aplicados = 0
    pos_aplicados = 0
    
    for variable in range(0,len(main_variables)):
        
        if str(main_variables[variable]) != '':
            variables_principales.append(main_variables[variable])
            filtros_aplicados[pos_aplicados].append(variables_principales[variable])
            
        if replace_value[variable] != '':
            variables_reemplazo.append(replace_value[variable])
            filtros_aplicados[pos_aplicados].append(variables_reemplazo[variable])
            
        if consecutives[variable] != '':
            variables_consecutivo.append(str(consecutives[variable]))
            filtros_aplicados[pos_aplicados].append(variables_consecutivo[variable])
            
        if pendientes[variable] != '':
            variables_pendientes.append(pendientes[variable])
            filtros_aplicados[pos_aplicados].append(variables_pendientes[variable])
                        
        if second_variables[variable] != '':
            variables_secundarias.append(second_variables[variable])
            filtros_aplicados[pos_aplicados].append(variables_secundarias[variable])
            
        if comparadores[variable] != '':
            variables_comparadores.append(comparadores[variable])
            filtros_aplicados[pos_aplicados].append(variables_comparadores[variable])
            
        if valores_comparadores[variable] != '':
            variables_comparacion.append(valores_comparadores[variable])
            filtros_aplicados[pos_aplicados].append(float(variables_comparacion[variable]))
        
        if acciones[variable] != '':
            variables_accion.append(acciones[variable])
            filtros_aplicados[pos_aplicados].append(variables_accion[variable])
        
        pos_aplicados+=1
        
    vector_filtros = [pos for pos in filtros_aplicados if pos != []] # vector de vectores que almacena todos los parametros de los filtros aplicados
    
    #elimino variable no utilizadas
    del(main_variables, second_variables, comparadores, valores_comparadores, acciones, filtros_aplicados)
    #luego de este paso me quedo con vectores que contienen unicamente las variables seleccionadas 
    
##############################################################################
################### APLICACION DE FILTROS ####################################
##############################################################################
# funcion de comparacion de dataframes principal vs filtrados    
    
# FILTRO DE DATOS Y PENDIENTES CONSECUTIVAS
    # para cada una de las variables seleccionadas se aplica el filtro
    # se crea un dataframe "filtrados" que donde se cumple la condición de datos consecutivos
    # se añade el índice a dicho dataframe
    # luego se aplica el where mirando la condición de si se repite el índice del dataframe principal
    # en el filtrados, en caso de que se repita se aplica la variable de reemplazo y si no el valor no cambia
   
    #dataframe para pendientes
    
    for var in range(0,len(variables_principales)):    
 
        # filtro de valores consecutivos
        # caso de accion "Reemplazar" 
        filtrados = datos.groupby((datos[variables_principales[var]].shift() != datos[variables_principales[var]]).\
                              cumsum()).filter(lambda x: len(x) >= int(variables_consecutivo[var]))  
        # esta linea transforma los datos no filtrados en str
        datos[variables_principales[var]] = np.where(datos.index.isin(filtrados.index), variables_reemplazo[var], datos[variables_principales[var]][:])
        
        # dataframe booleano de datos a filtrar
        a_filtrar = datos.index.isin(filtrados.index)
        
        # eliminacion de diezminutales que hayan sido filtrados previamente
        if variables_accion[var] == 'Eliminar diezminutal':
            for fila in range(0,len(df['fecha'])):
                if a_filtrar[fila]:
                        datos = datos.drop([fila])

    
    # aca convierto las columnas del dataframe en float antes de pasar a los filtros condicionales                
    for col in range(1,len(datos.columns)):      
        datos[datos.columns[col]] = pd.to_numeric(datos[datos.columns[col]]) 
            
# # FILTRO DE PENDIENTES CONSECUTIVAS    
    # pendientes = df.shift(periods = 1, fill_value = 0) #dataframe con datos corridos un lugar
    # print(pendientes)
    # for col in range(1, 
    #     for fila in range(0,len(df["fecha"])):
    
    #llamo funcion que aplica filtros
    filtrar_todos()    
    #dejo de contar tiempo
    elapsed_time = round((time.time() - start_time))
    print(f"Elapsed time: {elapsed_time}s")
    #escribo variable de estado que se muestra en ventana principal de la interfaz
    # global estado_txt
    estado_txt.set(time.strftime("%H:%M - ") + "Se aplican filtros seleccionados")
    # eliminar_columnas_repetidas()
    
    # habilitar botones de ventana de filtros
    exportar_csv.config(state = NORMAL)
    aplicar_huecos.config(state = NORMAL)
    eliminar_filtros.config(state = NORMAL)
    
    return datos                    
                        
# funcion que no hace nada, pero es necesaria para el funcionamiento de los combobox
def callback_function():
    print(combo[0].get())
    
# funcion para buscar archivos csv ya presentes en la carpeta principal
def busca_archivo_csv(directorio): #defino función para tomar lista de archivos
    return [obj.name for obj in scandir(directorio) if (obj.is_file() and os.path.splitext(obj)[1]==".csv")] #devuelvo lista de archivos en path 

# funcion que exporta datos con el boton "exportar" que se encuentra en la ventana de filtros
def exportar_filtrados():    
    global datos, estado_text, df
    
    # este if lo que hace es setear la columna fecha como el index del archivo a exportar
    # if len(df.columns == datos.columns):
    #     fecha = datos['fecha']
    #     datos = datos.drop(columns=['fecha'])
    #     datos = datos.set_index([fecha])
    
    datos.to_csv(str(ruta[1])+'_datos_filtrados.csv')
    estado_txt.set(time.strftime("%H:%M - ") + "Se exportan los datos filtrados")
    cuadro_dialogo_exportacion()
    # exec(open("v10.py", encoding="utf8", errors="ignore").read())

# funcion para que la interfaz grafica tome y muestre todas las variables seleccionadas cada vez que se agrega un atributo
def refresh():
    global directorio, datos, menu_variables
    file = busca_archivo_csv(directorio)
    print(file[0])
    datos = pd.read_csv(file[0])
    datos.drop("Unnamed: 0", axis="columns", inplace=True)
    menu_variables = []
    for columna in range(1,len(datos.columns)):
        menu_variables.append(datos.columns[columna])
    print(menu_variables)
    var1 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[0], state = 'readonly', width = 50).grid(row = 0, column = 0, pady = 3, padx = 5)
    var2 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[1], state = 'readonly', width = 50).grid(row = 1, column = 0, pady = 3, padx = 5)
    var3 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[2], state = 'readonly', width = 50).grid(row = 2, column = 0, pady = 3, padx = 5)
    var4 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[3], state = 'readonly', width = 50).grid(row = 3, column = 0, pady = 3, padx = 5)
    var5 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[4], state = 'readonly', width = 50).grid(row = 4, column = 0, pady = 3, padx = 5)
    var6 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[5], state = 'readonly', width = 50).grid(row = 5, column = 0, pady = 3, padx = 5)
    var7 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[6], state = 'readonly', width = 50).grid(row = 6, column = 0, pady = 3, padx = 5)
    var8 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[7], state = 'readonly', width = 50).grid(row = 7, column = 0, pady = 3, padx = 5)
    var9 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[8], state = 'readonly', width = 50).grid(row = 8, column = 0, pady = 3, padx = 5)
    var10 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[9], state = 'readonly', width = 50).grid(row = 9, column = 0, pady = 3, padx = 5)
    var11 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[10], state = 'readonly', width = 50).grid(row = 10, column = 0, pady = 3, padx = 5)
    var12 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[11], state = 'readonly', width = 50).grid(row = 11, column = 0, pady = 3, padx = 5)
    var13 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[12], state = 'readonly', width = 50).grid(row = 12, column = 0, pady = 3, padx = 5)
    var14 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[13], state = 'readonly', width = 50).grid(row = 13, column = 0, pady = 3, padx = 5)
    var15 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[14], state = 'readonly', width = 50).grid(row = 14, column = 0, pady = 3, padx = 5)
    segunda_var1 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[0], state = 'readonly', width = 50).grid(row = 0, column = 0, pady = 3, padx = 5)
    segunda_var2 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[1], state = 'readonly', width = 50).grid(row = 1, column = 0, pady = 3, padx = 5)
    segunda_var3 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[2], state = 'readonly', width = 50).grid(row = 2, column = 0, pady = 3, padx = 5)
    segunda_var4 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[3], state = 'readonly', width = 50).grid(row = 3, column = 0, pady = 3, padx = 5)
    segunda_var5 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[4], state = 'readonly', width = 50).grid(row = 4, column = 0, pady = 3, padx = 5)
    segunda_var6 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[5], state = 'readonly', width = 50).grid(row = 5, column = 0, pady = 3, padx = 5)
    segunda_var7 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[6], state = 'readonly', width = 50).grid(row = 6, column = 0, pady = 3, padx = 5)
    segunda_var8 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[7], state = 'readonly', width = 50).grid(row = 7, column = 0, pady = 3, padx = 5)
    segunda_var9 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[8], state = 'readonly', width = 50).grid(row = 8, column = 0, pady = 3, padx = 5)
    segunda_var10 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[9], state = 'readonly', width = 50).grid(row = 9, column = 0, pady = 3, padx = 5)
    segunda_var11 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[10], state = 'readonly', width = 50).grid(row = 10, column = 0, pady = 3, padx = 5)
    segunda_var12 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[11], state = 'readonly', width = 50).grid(row = 11, column = 0, pady = 3, padx = 5)
    segunda_var13 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[12], state = 'readonly', width = 50).grid(row = 12, column = 0, pady = 3, padx = 5)
    segunda_var14 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[13], state = 'readonly', width = 50).grid(row = 13, column = 0, pady = 3, padx = 5)
    segunda_var15 = ttk.Combobox(encuadre_4, values = menu_variables, textvariable = combo2[14], state = 'readonly', width = 50).grid(row = 14, column = 0, pady = 3, padx = 5)
     
# borrar archivos csv previamente dejados en la carpeta 
def borrar_archivos_csv():
    try:
        eliminado = busca_archivo_csv(directorio)
        for file in eliminado:
            remove(file)
            print("Se elimina arhivo:")
            print(file)
    except:
        print("No se detectan archivos previos...")
        pass        
        
# funcion que compara strings devolviendo un ratio de coincidencia
def comparar_strings(string1,string2):
    global diferencia
    secuencia = dlb.SequenceMatcher(isjunk = None,a=str(string1),b=str(string2))
    diferencia = round(secuencia.ratio()*100,1)
    return diferencia
    
# funcion para aplicar los filtros en todos las variables
# no funciona tan lenta como pense
def filtrar_todos():    
    global vector_filtros, estado_txt
    estado_txt.set("Aplicando filtros...")
    barra1.stop()
    # aplico filtro unicamente en variables seleccionadas dentro del vector de filtros
    for var in range(0,len(vector_filtros)):
        filtrar_condicionales_2(vector_filtros[var][0],var,vector_filtros)
        # filtros_rapidos(vector_filtros[var][0], var, vector_filtros)
    
    # voy a probar hacer que por cada coincidencia entre variables
    # se sobre escriba la que esta en el vector de filtros
    vector_filtros_auxiliar = vector_filtros # vector auxiliar para modificar
    for filtro in range(0,len(vector_filtros)):    
        for col in range(1,len(datos.columns)):
            if comparar_strings(datos.columns[col],vector_filtros[filtro][0])>95.5 and comparar_strings(datos.columns[col],vector_filtros[filtro][0]) !=100:
                vector_filtros_auxiliar[filtro][0] = datos.columns[col] 
                filtrar_condicionales_2(vector_filtros_auxiliar[filtro][0], filtro, vector_filtros_auxiliar)
                # filtros_rapidos(vector_filtros_auxiliar[filtro][0], filtro, vector_filtros_auxiliar)
    
            barra1['value'] += 100/col
            ventana.update_idletasks()
    # eliminar_columnas_repetidas()

# funcion de filtros mejorada NO IMPLEMENTADA
def filtros_rapidos(variable,pos,filtros):
    global datos
    
    if filtros[pos][5] == condiciones[0]:
        if filtros[pos][7] == accion[0]:
            datos.loc[datos[str(variable)] < filtros[pos][6], str(variable)] = filtros[pos][1]
                
    elif filtros[pos][5] == condiciones[1]:
        if filtros[pos][7] == accion[0]:
            datos.loc[datos[str(variable)] > filtros[pos][6], str(variable)] = filtros[pos][1]
                
    elif filtros[pos][5] == condiciones[2]:
        if filtros[pos][7] == accion[0]:
            datos.loc[datos[str(variable)] == filtros[pos][6], str(variable)] = filtros[pos][1]
        
    elif filtros[pos][5] == condiciones[3]:
        if filtros[pos][7] == accion[0]:
            datos.loc[datos[str(variable)] != filtros[pos][6], str(variable)] = filtros[pos][1]
                
    elif filtros[pos][5] == condiciones[4]:
        if filtros[pos][7] == accion[0]:
            datos.loc[datos[str(variable)] <= filtros[pos][6], str(variable)] = filtros[pos][1]
                
    elif filtros[pos][5] == condiciones[5]:
        if filtros[pos][7] == accion[0]:
            datos.loc[datos[str(variable)] >= filtros[pos][6], str(variable)] = filtros[pos][1]
           
    return datos

# funciones de filtros separadas individualmente    
def filtrar_consecutivos(variable):
    global datos,vector_filtros
    filtrados = datos.groupby((datos[variable].shift()!=datos[variable]).\
                              cumsum()).filter(lambda x: len(x)>=int(vector_filtros[0][2]))
    datos[variable] = np.where(datos.index.isin(filtrados.index),vector_filtros[0][1],datos[variable])
    
# nuevo filtro de condicionales
# funcion para filtrar condicionales
def filtrar_condicionales_2(variable,pos,filtro):
    global datos
    date = pd.DataFrame(datos['fecha'])  
        
    if comparar_strings(variable, filtro[pos][0]) > 93.9:
                
        # recorro dataframe para filtrar
        for index in datos.index:
            # ahora evaluo condicion de comparacion
            # pregunto condiciones de filtrado y 
            if filtro[pos][5]==condiciones[0]: 
                # condicion "menor que"
                if float(datos[variable][index])<float(filtro[pos][6]):
                    # evaluo accion a tomar en el filtro
                    # reemplazar 
                    if filtro[pos][7]==accion[0]:
                        datos[variable][index]=str(filtro[pos][1])
                    elif filtro[pos][7]==accion[1]:
                        datos.iloc[index,:] = float(filtro[pos][1])
                        datos['fecha'][index] = date['fecha'][index]
                    elif filtro[pos][7]==accion[2]:
                        datos = datos.drop([index])
                        
            # ahora evaluo condicion de comparacion
            # pregunto condiciones de filtrado y 
            if filtro[pos][5]==condiciones[1]: 
                # condicion "menor que"
                if float(datos[variable][index])>float(filtro[pos][6]):
                    # evaluo accion a tomar en el filtro
                    # reemplazar 
                    if filtro[pos][7]==accion[0]:
                        datos[variable][index]=str(filtro[pos][1])
                    elif filtro[pos][7]==accion[1]:
                        datos.iloc[index,:] = float(filtro[pos][1])
                        datos['fecha'][index] = date['fecha'][index]
                    elif filtro[pos][7]==accion[2]:
                        datos = datos.drop([index])
            
            # ahora evaluo condicion de comparacion
            # pregunto condiciones de filtrado y 
            if filtro[pos][5]==condiciones[2]: 
                # condicion "menor que"
                if float(datos[variable][index])==float(filtro[pos][6]):
                    # evaluo accion a tomar en el filtro
                    # reemplazar 
                    if filtro[pos][7]==accion[0]:
                        datos[variable][index]=str(filtro[pos][1])
                    elif filtro[pos][7]==accion[1]:
                        datos.iloc[index,:] = float(filtro[pos][1])
                        datos['fecha'][index] = date['fecha'][index]
                    elif filtro[pos][7]==accion[2]:
                        datos = datos.drop([index])
            
            # ahora evaluo condicion de comparacion
            # pregunto condiciones de filtrado y 
            if filtro[pos][5]==condiciones[3]: 
                # condicion "menor que"
                if float(datos[variable][index])!=float(filtro[pos][6]):
                    # evaluo accion a tomar en el filtro
                    # reemplazar 
                    if filtro[pos][7]==accion[0]:
                        datos[variable][index]=str(filtro[pos][1])
                    elif filtro[pos][7]==accion[1]:
                        datos.iloc[index,:] = float(filtro[pos][1])
                        datos['fecha'][index] = date['fecha'][index]
                    elif filtro[pos][7]==accion[2]:
                        datos = datos.drop([index])
                        
            # ahora evaluo condicion de comparacion
            # pregunto condiciones de filtrado y 
            if filtro[pos][5]==condiciones[4]: 
                # condicion "menor que"
                if float(datos[variable][index])<=float(filtro[pos][6]):
                    # evaluo accion a tomar en el filtro
                    # reemplazar 
                    if filtro[pos][7]==accion[0]:
                        datos[variable][index]=str(filtro[pos][1])
                    elif filtro[pos][7]==accion[1]:
                        datos.iloc[index,:] = float(filtro[pos][1])
                        datos['fecha'][index] = date['fecha'][index]
                    elif filtro[pos][7]==accion[2]:
                        datos = datos.drop([index])
            
            # ahora evaluo condicion de comparacion
            # pregunto condiciones de filtrado y 
            if filtro[pos][5]==condiciones[5]: 
                # condicion "menor que"
                if float(datos[variable][index])>=float(filtro[pos][6]):
                    # evaluo accion a tomar en el filtro
                    # reemplazar 
                    if filtro[pos][7]==accion[0]:
                        datos[variable][index]=str(filtro[pos][1])
                    elif filtro[pos][7]==accion[1]:
                        datos.iloc[index,:] = float(filtro[pos][1])
                        datos['fecha'][index] = date['fecha'][index]
                    elif filtro[pos][7]==accion[2]:
                        datos = datos.drop([index])

# cuadro de dialogo para exportacion de archivos filtrados                
def cuadro_dialogo_exportacion():
    from tkinter import messagebox
    file = [obj.name for obj in scandir(directorio) if (obj.is_file() and os.path.splitext(obj)[1]==".csv")] #devuelvo lista de archivos en path 
    csv_sin_filtro = 'Archivo con datos crudos: '
    csv_con_filtro = 'Archivos con datos filtrados: '
    messagebox.showinfo(message="Carpeta: "+directorio+'\n'+csv_sin_filtro+file[0]+'\n' +csv_con_filtro+file[1], title='Información de los archivos exportados')
    # messagebox.showinfo('Los archivos se encuentran en la carpeta: '+directorio+', '+message=csv_sin_filtro+file[0]+', '+csv_con_filtro+file[1], title="Archivos Exportados")
    
# funcion para filtrar variables que se cargan dos veces por error
def eliminar_columnas_repetidas():
    global datos
    columnas = datos.columns[1,-1]
    indx_col = 1
    
    for col in range(2,len(datos.columns)):
        if datos[datos.columns[indx_col]].mean() == datos[datos.columns[col]].mean():
            datos = datos.drop([datos.columns[col]])
            
        if col == len(datos.columns)-2:
            indx_col+=1
            
# funcion de boton para reemplazar datos filtrados por huecos
def aplicar_huecos_en_filtrados():
    global datos, vector_filtros, estado_txt
    
    hueco = str(" ")    # variable de hueco
    fecha = datos['fecha']    # guardar a parte el vector de fechas  
    datos = datos.drop(columns = ['fecha']) # dropeo vector de fechas para que facilitar el analisis
    
    valor_reemplazo = float(vector_filtros[0][1])
 
    # suprime advertencias
    warnings.simplefilter(action='ignore', category=FutureWarning)
        
    for col in datos.columns:
        datos.loc[datos[col] == valor_reemplazo, str(col)]= hueco
        
    datos = datos.set_index([fecha]) # seteo fechas como index    
    estado_txt.set("Se aplican huecos a todos los valores filtrados")

# funcion de boton de eliminar filtros seleccionados
def eliminar_filtros_aplicados():
    global df, datos, estado_txt
    datos = df
    refresh()
    estado_txt.set('Se eliminan todos los filtros aplicados')

##########################################################
############# FUNCIONES DE VENTANA GRAFICA ###############
##########################################################
# actualizar variables en ventana grafica
def actualizar_ventana_grafica():
    global variables_graficar, checkbox_variables, checkVar, chosen
    variables_graficar = df.columns
    # variables para checkbox
    checkbox_variables = []
    checkVar = []
    chosen = []
    for i in range(0,len(variables_graficar)):
        checkbox_variables.append(variables_graficar[i])
        checkVar.append(tkinter.StringVar())
        chosen.append("object")    
    
    # checks para seleccion de variables
    for var in range(1,len(variables_graficar)):
        checkbox_variables[var] = tkinter.Checkbutton(grf_cuadro_variables, 
                                                      text = " ").grid(row = var, column = 0, 
                                                          pady = 5, padx = 5, sticky = W)
        
        checkbox_variables[var] = tkinter.Checkbutton(grf_cuadro_variables, 
                                                      variable = checkVar[var], 
                                                      text = variables_graficar[var]).grid(row = var, column = 0, 
                                                          pady = 5, padx = 5, sticky = W)

#funcion para checkear el estado de los checkbox
def check_clicked():
    if checkVar[1].get(): print("se selecciona variable")
    elif checkVar[1].get()==0: print("se deselecciona")

# funciones de botones para graficar
# funciones gráficas
def histograma():
    global datos    
    # establezco fecha como eje x
    ejeX = df['fecha']
    plt.xlabel("Fecha", fontsize=12)
    # el eje Y sera un vector que almacene todas las otras columnas
    ejeY = []
    indx = 0    
    for var in range(1,len(checkVar)):
        if checkVar[var].get():
            ejeY.append(datos.columns[var])            
            fig, ax = plt.subplots()
            # ax.plot(ejeX, df[ejeY[indx]])
            ax.hist(datos[ejeY[indx]], bins=round(math.sqrt(len(df["fecha"]))))
            ax.set_title('Histograma '+str(datos.columns[var][8:13])+str(datos.columns[var][16:50]))                                                                                              
            # ax.set_xlabel("Fecha")
            # ax.set_xlabel(str(df.columns[var][8:13])+str(df.columns[var][16:50]))
            indx+=1   
            plt.grid()
        plt.show()

def evolucion_temporal():
    global datos
    # establezco fecha como eje x
    ejeX = df['fecha']
    plt.xlabel("Fecha", fontsize=12)
    # el eje Y sera un vector que almacene todas las otras columnas
    ejeY = []
    indx = 0    
    for var in range(1,len(checkVar)):
        if checkVar[var].get():
            ejeY.append(datos.columns[var])            
            fig, ax = plt.subplots()
            ax.plot(ejeX, datos[ejeY[indx]])
            ax.set_title('Evolucion Temporal')                                                                                              
            ax.set_xlabel("Fecha")
            ax.set_ylabel(str(datos.columns[var][8:13])+str(datos.columns[var][16:50]))
            indx+=1   
            plt.grid()
        plt.show()
        plt.clf()
               
###########################################################
########## FUNCIONES CARGA DE DATOS PREDEFINIDOS ##########
###########################################################
def levantar_datos_adme():
    print(parque_adme.get())
    global atributos_seleccionados, atributos_finales, atributos_PI
    
    if parque_adme.get()=='ARTILLEROS':
        atributos_seleccionados = []
    elif parque_adme.get()=='ARIAS':
        atributos_seleccionados = ['EOL_ARI_MET01_10_Average_DirAlt1',
                                    'EOL_ARI_MET01_10_Average_DirAlt2',
                                    'EOL_ARI_MET01_10_Average_HumRelInst',
                                    'EOL_ARI_MET01_10_Average_PresAtmInst',
                                    'EOL_ARI_MET01_10_Average_TempInst',
                                    'EOL_ARI_MET01_10_Average_VelHorizMediaAlt1',
                                    'EOL_ARI_MET01_10_Average_VelHorizMediaAlt2']
    elif parque_adme.get()=='CARACOLES':
        atributos_seleccionados = []
    elif parque_adme.get()=='JUAN PABLO TERRA':
        atributos_seleccionados = ['EOL_JPT_MET01_10_AD10Min_Average_ANA0',
                                    'EOL_JPT_MET01_10_AD10Min_Average_ANA1',
                                    'EOL_JPT_MET01_10_AD10Min_Average_ANA4',
                                    'EOL_JPT_MET01_10_AD10Min_Average_ANA5',
                                    'EOL_JPT_MET01_10_AD10Min_Average_ANA11',
                                    'EOL_JPT_MET01_10_AD10Min_Average_ANA2',
                                    'EOL_JPT_MET01_10_VEL_VIENTO_FICT_CALC']
    elif parque_adme.get()=='PALOMAS':
        atributos_seleccionados=['EOL_PAL_MET01_10_Average_DirAlt1',
                                  'EOL_PAL_MET01_10_Average_HumRelInst1',
                                  'EOL_PAL_MET01_10_Average_PresAtmInst1',
                                  'EOL_PAL_MET01_10_Average_VelHorizMediaAlt1',
                                  'EOL_PAL_MET01_10_Deviation_VelHorizMediaAlt2']
    elif parque_adme.get()=='PAMPA':
        atributos_seleccionados=['EOL_PAM_MET01_10_AD10Min_Average_ANA0',
                                  'EOL_PAM_MET01_10_AD10Min_Average_ANA8',
                                  'EOL_PAM_MET01_10_AD10Min_Average_ANA1',
                                  'EOL_PAM_MET01_10_AD10Min_Average_ANA12',
                                  'EOL_PAM_MET01_10_AD10Min_Average_ANA14',
                                  'EOL_PAM_MET01_10_AD10Min_Average_ANA16']
    elif parque_adme.get()=='VALENTINES':
        atributos_seleccionados = ['EOL_ARI_MET01_10_Average_DirAlt1',
                                    'EOL_ARI_MET01_10_Average_DirAlt2',
                                    'EOL_ARI_MET01_10_Average_HumRelInst',
                                    'EOL_ARI_MET01_10_Average_PresAtmInst',
                                    'EOL_ARI_MET01_10_Average_TempInst',
                                    'EOL_ARI_MET01_10_Average_VelHorizMediaAlt1',
                                    'EOL_ARI_MET01_10_Average_VelHorizMediaAlt2']
    # print(atributos_seleccionados)
    atributos_finales = atributos_seleccionados
    ruta.append(atributos_seleccionados[0][4:7])
    ruta.append(atributos_seleccionados[0][4:7])
    ruta.append(atributos_seleccionados[0][8:13])
    print(atributos_finales)
    
    cargar_datos_predefinidos(atributos_seleccionados)
        
# funcion para levantar datos predefinidos para curva de potencia
def levantar_datos_cdp():
    global atributos_seleccionados, atributos_finales, atributos_PI, aerogens
    
    # variable global para almacenar ag donde se replicaran datos
    # aerogens.append(ag_cdp.get())
        
    if parque_cdp.get()=='ARIAS':
        atributos_finales = [
        "EOL_ARI_MET01_10_Average_PresAtmInst",
        "EOL_ARI_AG01_10_Average_PotActiva",
        "EOL_ARI_AG01_10_Average_VelViento",
        "EOL_ARI_AG01_10_Average_TempAmb",
        "EOL_ARI_AG01_10_EstadoMasRestrictivoCalc",
        ]
        # atributos_seleccionados = atributos_finales
        variables_met = atributos_finales[0]
        atributos_finales.pop(0)
        cambiar_ag_atributos(atributos_finales, ag_cdp.get())
  
    elif parque_cdp.get()=='ARTILLEROS':
        atributos_seleccionados = []
    
    elif parque_cdp.get()=='CARACOLES':
        atributos_finales = [
        "EOL_CAR_MET01_SS_Pressure",
        "EOL_CAR_AG01_10_GRD_PROD_PWR_AVG",
        "EOL_CAR_AG01_10_AMB_WINDSPEED_AVG",
        "EOL_CAR_AG01_10_AMB_TEMP_AVG",
        "EOL_CAR_AG01_10_SYS_STATS_TRBSTAT",
            ]
        variables_met = atributos_finales[0]
        atributos_finales.pop(0)
        cambiar_ag_atributos(atributos_finales, ag_cdp.get())
        
    elif parque_cdp.get()=='JUAN PABLO TERRA':
        atributos_finales = [
       'EOL_JPT_AG01_10_AD10Min_Average_ANA067',
       "EOL_JPT_AG01_10_AD10Min_Average_ANA008",
       "EOL_JPT_AG01_10_AD10Min_Average_ANA016",
       "EOL_JPT_AG01_10_AD10Min_Average_ANA029",
       "EOL_JPT_AG01_10_AD10Min_Average_ANA107",
       ]
        cambiar_ag_atributos(atributos_finales, ag_cdp.get())
        
    elif parque_cdp.get()=='PALOMAS':
        atributos_finales = [
        "EOL_PAL_MET01_10_Average_PresAtmInst1",
        "EOL_PAL_AG01_10_GRD_PROD_PWR_AVG",
        "EOL_PAL_AG01_10_AMB_WINDSPEED_AVG",
        "EOL_PAL_AG01_10_AMB_TEMP_AVG",
        "EOL_PAL_AG01_10_SYS_STATS_TRBSTAT",
        ]
        variables_met = atributos_finales[0]
        atributos_finales.pop(0)
        cambiar_ag_atributos(atributos_finales, ag_cdp.get())
    
    elif parque_cdp.get()=='PAMPA':
        atributos_finales = [
        'EOL_PAM_AG01_10_AD10Min_Average_ANA067',
        "EOL_PAM_AG01_10_AD10Min_Average_ANA008",
        "EOL_PAM_AG01_10_AD10Min_Average_ANA016",
        "EOL_PAM_AG01_10_AD10Min_Average_ANA029",
        "EOL_PAM_AG01_10_AD10Min_Average_ANA107",
        ]
        cambiar_ag_atributos(atributos_finales, ag_cdp.get())
    
    elif parque_cdp.get()=='VALENTINES':
        atributos_finales = [
        "EOL_VAL_MET01_10_Average_PresAtmInst",
        "EOL_VAL_AG01_10_Average_PotActiva",
        "EOL_VAL_AG01_10_Average_VelViento",
        "EOL_VAL_AG01_10_Average_TempAmb",
        "EOL_VAL_AG01_10_EstadoMasRestrictivoCalc",
        ]
        variables_met = atributos_finales[0]
        atributos_finales.pop(0)
        cambiar_ag_atributos(atributos_finales, ag_cdp.get())
                    
    # atributos_seleccionados = atributos_finales
    ruta.append(atributos_finales[0][4:7])
    ruta.append(atributos_finales[0][4:7])
    ruta.append(atributos_finales[0][8:13])
    
    # cargar_datos_predefinidos(atributos_seleccionados)
    atributos_PI = atributos_finales
    atributos_seleccionados = atributos_finales
    
    # cargar variable de met en atributos donde se tuvo que extraer
    if len(variables_met)>0:
        atributos_finales.append(variables_met)    
    
    cargar_datos_predefinidos(atributos_finales) #funcion de cargar datos
    #mejorar esto, no puede haber 3 funciones de carga de datos, mono incapaz

# funcion para cambiar ag en atributos
def cambiar_ag_atributos(atributos,aero):
    if atributos[0][8:12] != aero:
        for atr in range(0,len(atributos)):
            atributos[atr] = atributos[atr].replace('AG01',aero)
    return atributos

def cargar_datos_predefinidos(variables):
    
    from tqdm import tqdm
    global estado_text, atributos_PI, df, datos
    
    estado_txt.set("Cargando set de datos predefinidos...")
    
    #Periodo y rango de fechas  
    fecha_inicio = fecha_ini_var.get()
    fecha_fin = fecha_fin_var.get()
    timerange = AFTimeRange(fecha_inicio, fecha_fin)
    
    # atributos para consulta
    atributos_PI = []
    # agrego los afdata correspondientes al nombre del tag
    for senal in variables:
        atributos_PI.append(PIPoint.FindPIPoint(piServer, senal))
        
    #Genero las fechas ordenadas
    fecha_inicio_time=datetime.strptime(fecha_inicio,'%d/%m/%Y %H:%M')
    fecha_inicio_num=date2num(fecha_inicio_time)
    fecha_fin_time=datetime.strptime(fecha_fin,'%d/%m/%Y %H:%M')
    fecha_fin_num=date2num(fecha_fin_time)
    
    rango_fechas=pd.date_range(start=fecha_inicio_time, end=fecha_fin_time, freq="10min")
    indice_fechas=range(0,len(rango_fechas))
    
    #Genero DataFrame para guardar los datos consultado
    global df
    df=pd.DataFrame({"fecha":rango_fechas},index=indice_fechas)
    
    #Consulta de datos
    #Se consultan los datos para cada elemento de atributos_PI
    for consulta in tqdm(range(0,len(atributos_PI))):
        variables[consulta] = atributos_PI[consulta].Name     
        nombre_atributo = atributos_PI[consulta].Name
        
        
        
        #Genero tres arrays vacíos para guardar los datos conultados
        fecha=[]
        datos=[]
        indice=[]

        #Variable para verificar ausencia de fechas repetidas
        fecha_anterior=datetime(1990,10,6,1,50)
    
        #Defino un DataFrame auxiliar para guardar los datos de un elemento
        df_aux=pd.DataFrame()
        
        resultado = atributos_PI[consulta].RecordedValues(timerange, AFBoundaryType.Inside, "", False)
    
        #Recorro todos los elementos del resulado de la consulta para...
        #...agregar los datos en los vectores correspondientes
        for event in resultado:

            #Solo agrego datos que conicidan con diezminutales
            if (event.Timestamp.LocalTime.Minute%10==0)and(event.Timestamp.LocalTime.Second==0):
            
                #Convierto al tipo datetime
                fecha_aux=datetime(event.Timestamp.LocalTime.Year,
                               event.Timestamp.LocalTime.Month,
                               event.Timestamp.LocalTime.Day,
                               event.Timestamp.LocalTime.Hour,
                               event.Timestamp.LocalTime.Minute)
            
                if fecha_aux!=fecha_anterior:
                
                    #Agrego fecha al vector
                    fecha.append(fecha_aux)

                    #Agrego dato al vector
                    datos.append(event.Value)
                    #Agrego su indice relativo a la fecha de inicio
                    indice.append(round((date2num(fecha_aux)*6*24)-(fecha_inicio_num*6*24)))
                    fecha_anterior=fecha_aux        
               
        nombre_columna2=nombre_atributo
        df_aux1=pd.DataFrame({nombre_columna2:datos},index=indice)
        df=pd.concat([df,df_aux1], axis=1, sort=False)
        
        #convertir dataframe a valores numericos
        #cuando el contenido no es numerico pone un NaN en su lugar
        df_2 = df.apply(pd.to_numeric,errors='ignore')
        
        #cuando hago esta conversion tambien convierte el vector de fechas a numerico
        #por lo tanto tengo que volver el vector de fechas a su estado original
        df_2['fecha'] = df['fecha']
        
        #luego de que df_2 queda con el la columna de fechas correcta, lo vuelvo a convertir en df
        df = df_2
        
        # filtrar nan
        df = df.fillna("")
        
        #cargar y actualizar barra de carga
        barra1['value']+=100/len(atributos_PI)
        ventana.update_idletasks()
       
        # funcion para eliminar columnas repetidas 
        # eliminar_columnas_repetidas(df)
        
    
    # exporto datos
    df.to_csv(str(ruta[1])+'_datos_crudos.csv')
    
    estado_txt.set(time.strftime("%H:%M - ") + "Se cargan los datos satisfactoriamente")
    refresh()
    #habilito botones inicialmente deshabilitados 
    btn_crear_atributos.config(state = NORMAL)
    
    lista_variables()    
    refresh() #actualiza variables en ventana de filtros    

##########################################################################
########################CONFIGURACION GUI####################################
#############################################################################
#DECLARACION DE VARIABLES GLOBALES

#array para guardar ruta del objeto 
ruta = []

#conexion a servidor
connect_to_PISystem('PIDataCollective')
connect_to_Server('PIDataCollective')

#se crea dataframe de pandas para contener los datos cargados
df = datos = pendientes = pd.DataFrame()

#variable globales
listado_actual = []
listado_atributos_actual = []
atributos_seleccionados = []
objeto_seleccionado = piSystem
listado_actual.append(objeto_seleccionado)
atributos_PI = []
#variables para aerogeneradores
aerogens = []
#variables que almacena los atributos creados para todos los ags
atributos_finales = []
#filtros condicionales
# # #Variables para filtrado de datos
combo = replace = consecutivo_ = pendiente_ = combo2 = comparador = compare_value = accion_ = []

##############################################################################
######################### VARIABLES GLOBALES FILTRADO ########################
##############################################################################
# directrio donde buscar datos a filtrar
# directorio = '//ntpal/grupos2/Eolica/2. INGENIERÍA/04.- Sistemas informáticos/Desarrollos Python/Consulta de datos PI/Interfaz gráfica/version actual/piQuery - filtros separados'
directorio = os.getcwd()
print(directorio)
# directorio = '//ntpal/grupos2/MedicionesEolicas/PI/python'
menu_variables = []   

# \\ntpal\grupos2\MedicionesEolicas\PI\python

try: 
    file = [obj.name for obj in scandir(directorio) if (obj.is_file() and os.path.splitext(obj)[1]==".csv")] #devuelvo lista de archivos en path 
    print(file[0])
    datos = pd.read_csv(file[0])
    datos.drop('Unnamed: 0',axis='columns', inplace=True)
    #variable de variables para menu desplegable
    for columna in range(1,len(datos.columns)):
        menu_variables.append(datos.columns[columna])
except:
    pass

borrar_archivos_csv()
    
#opciones de menues desplegables
condiciones = ['<', '>', '=', '!=', '<=', '>=']
accion = ['Reemplazar', 'Reemplazar varios', 'Eliminar diezminutal']
vector_filtros = [] # array para almacenar filtros aplicados 
##############################################################################

# VENTANA PRINCIPAL
ventana = tkinter.Tk()
ventana.title('piQuery - consulta de datos PI')

# CREACION DE PESTAÑAS
nb = ttk.Notebook(ventana)
nb.grid(row = 1, column = 0, padx = 5, pady = 5)
# Pestaña de filtros
consulta = ttk.Frame(nb)
filtrados = ttk.Frame(nb)
graficar = ttk.Frame(nb)

# continua en últimas lineas

#SELECCION DE ELEMENTOS Y ATRIBUTOS
#cuadro de trabajo principal
main_cuadro = tkinter.LabelFrame(consulta)
main_cuadro.grid(row = 1, column = 0, pady = 2, padx = 5, sticky = W + S + E + N)
#cuadro de texto "selecion de periodo"
cuadro = tkinter.LabelFrame(main_cuadro, text = "Parámetros de consulta")#este cuadro quedo sin titulo
cuadro.grid(row = 1, column = 0, pady = 10, padx = 5, sticky = W + E)
#etiqueta de ruta
mostrar_ruta = StringVar() # variables para escribir texto en ventana
mostrar_ruta.set('')
ruta_label = tkinter.Label(cuadro, textvariable = mostrar_ruta, fg = 'red').grid(row = 6, column = 0, columnspan = 5, sticky = W + E)

# #logo
# logo = tkinter.PhotoImage(file='logo.png')
# logo_label = tkinter.Label(ventana, image = logo)
# logo_label.grid(row = 0, column = 0, columnspan = 3, padx = 30, pady = 5, sticky = N + W)
logo = tkinter.Label(ventana, text = 'piQuery')
logo.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = S)
logo.config(fg = 'black', font = ('Bahnschrift SemiLight Condensed',30))
# etiqueta logo
info_logo = tkinter.Label(ventana, text = 'Interfaz de consulta de datos PI')
info_logo.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = S)
# logo.config(fg = 'black', font = ('Bahnschrift SemiLight Condensed',25))

#cuadro de seleccion de variables
select_var_cuadro = tkinter.LabelFrame(cuadro, text = "Seleccione variables a trabajar")
select_var_cuadro.grid(row = 0, column = 1, columnspan = 3, pady = 5, padx = 5, sticky = N + S)
#seleccion de periodo
frame_fechas = tkinter.LabelFrame(cuadro, text = "Selección de periodo")
frame_fechas.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = N + S)

#etiqueta elementos
lista_elementos_label = tkinter.Label(select_var_cuadro, text = "Elementos").grid(row = 2, column = 2, pady = 1, padx = 2)
#lista de seleccion de elementos
scroll_elementos = tkinter.Scrollbar(select_var_cuadro, orient = VERTICAL)
lista_elementos = tkinter.Listbox(select_var_cuadro, width = 40, yscrollcommand=scroll_elementos.set)
lista_elementos.grid(row = 3 , column = 2)
scroll_elementos.config(command = lista_elementos.yview)
scroll_elementos.grid(row = 3, column = 3)

#BOTONES SELECCIONAR Y RETROCECEDER
desplegar_boton = tkinter.Button(select_var_cuadro, text = '--->', command = avanzar).grid(row = 4, column = 2, pady = 3, padx = 5, sticky = E)
back_boton = tkinter.Button(select_var_cuadro, text = '<---', command = retroceder).grid(row = 4, column = 2, pady = 3, padx = 5, sticky = W)

lista_elementos.bind('<Double-Button>', avanzar_dblclick)

#SELECCION DE ATRIBUTOS
lista_atributos_label = tkinter.Label(select_var_cuadro, text = "Atributos").grid(row = 2, column = 4, pady = 1, padx = 2)
#lista de seleccion de atributos
scroll_atributos = tkinter.Scrollbar(select_var_cuadro, orient = VERTICAL)
lista_atributos = tkinter.Listbox(select_var_cuadro, width = 50, yscrollcommand=scroll_atributos.set)
lista_atributos.grid(row = 3 , column = 4)
scroll_atributos.config(command = lista_atributos.yview)
scroll_atributos.grid(row = 3, column = 5)
#BOTON SELECCIONAR
select_boton = tkinter.Button(select_var_cuadro, text = "Seleccionar", command = agregar_seleccion).grid(row = 4, column = 4, pady = 3)

lista_atributos.bind('<Double-Button>', agregar_seleccion_dblclick)

#VARIABLES SELECCIONADAS
lista_seleccionados_label = tkinter.Label(select_var_cuadro, text = "Variables seleccionadas").grid(row = 2, column = 6, pady = 1, padx = 2)
#lista de variables seleccionadas
scroll_seleccionados = tkinter.Scrollbar(select_var_cuadro, orient = VERTICAL)
lista_seleccionados = tkinter.Listbox(select_var_cuadro, width = 80, yscrollcommand=scroll_seleccionados.set)
lista_seleccionados.grid(row = 3 , column = 6)
scroll_seleccionados.config(command = lista_seleccionados.yview)
scroll_seleccionados.grid(row = 3, column = 7)
#BOTON ELIMINAR
delete_boton = tkinter.Button(select_var_cuadro, text = 'Quitar', command = quitar_seleccion).grid(row = 4, column = 6, pady = 3)

#texto etiqueta de estado
estado_txt = StringVar()
estado_txt.set('')
#etiqueta de estado

# # loading bar
barra1 = ttk.Progressbar(ventana, orient=HORIZONTAL, length=900, mode='determinate')
barra1.grid(row=10, column=0, pady=5, padx=5)

#fechas-->etiquetas, variables,seteo inicial
fecha_ini_lbl = tkinter.Label(frame_fechas, text = 'Fecha de Inicio').grid(row = 1, column = 0, padx = 5)
fecha_ini_var = StringVar()
fecha_ini_var.set('01/01/2020 00:00')
fecha_ini_entry = tkinter.Entry(frame_fechas, textvariable = fecha_ini_var).grid(row = 2, column = 0, padx = 5, pady = 5)

fecha_fin_lbl = tkinter.Label(frame_fechas, text = 'Fecha de Fin').grid(row = 3, column = 0, padx = 5)
fecha_fin_var = StringVar()
fecha_fin_var.set('01/06/2020 23:50')
fecha_fin_entry = tkinter.Entry(frame_fechas, textvariable = fecha_fin_var).grid(row = 4, column = 0, padx = 5, pady = 5)

#boton de carga -- crea dataframe
cargar_datos = tkinter.Button(frame_fechas, text = 'Cargar', command = cargarDatos).grid(row = 5, column = 0, rowspan = 3, pady = 5, padx = 5, sticky = W + E + N + S)

#etiqueta de estado
estado = tkinter.Label(ventana, textvariable = estado_txt, fg = 'red').grid(row = 11, column = 0, columnspan = 3, sticky = W + E)

##############################################################################
################### REPLICAR DATOS PARA OTROS AGs ############################
##############################################################################

#cuadro de adorno
cuadro_sin_name = tkinter.LabelFrame(main_cuadro)
cuadro_sin_name.grid(row = 3, column = 0, sticky = N + W, pady = 5, padx = 5)
#cuadro aerogeneradores principal
ags_var_cuadro = tkinter.LabelFrame(cuadro_sin_name, text = "Replicar variables para otros Ags")
ags_var_cuadro.grid(row = 1, column = 1, padx = 5, sticky = N + E, pady = 5)

#cuadro de seleccion de aerogeneradores
ags_sel_cuadro = tkinter.LabelFrame(ags_var_cuadro, text = "Seleccion de aerogeneradores")
ags_sel_cuadro.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = W + E + N + S)

# VARIABLES SELECCIONADAS
var_selected_lbl = tkinter.Label(ags_sel_cuadro, text = "Variables seleccionadas").grid(row = 0, column = 1, pady = 1, padx = 5)
#lista de variables seleccionadas
scroll_var_selected = tkinter.Scrollbar(ags_sel_cuadro, orient = VERTICAL)
lista_var_selected = tkinter.Listbox(ags_sel_cuadro, width = 40, height = 10, yscrollcommand=scroll_var_selected.set)
scroll_var_selected.config(command = lista_var_selected.yview)
scroll_var_selected.grid(row = 1, column = 2)
lista_var_selected.grid(row = 1 , column = 1)

#aerogenerador de referencia del cual se sacan las variables a replicar en los otros
ag_actual = StringVar()
ag_actual.set("AG")
lbl_ag = tkinter.Label(ags_sel_cuadro, text = "AG actual").grid(row = 0, column = 0, padx = 2, pady = 5)
lbl_ag_select = tkinter.Label(ags_sel_cuadro, textvariable = ag_actual).grid(row = 1, column = 0, padx = 2, pady = 5, sticky = N)

#LISTA AEROS
ag_list_lbl = tkinter.Label(ags_sel_cuadro, text = "Lista de AGs").grid(row = 0, column = 4, pady = 1, padx = 2, )
# btn_load_ags = tkinter.Button(ags_sel_cuadro, text = "Lista AGs", command = lista_ags).grid(row = 2, column = 4, pady = 5, padx = 5, sticky = W + E)  
scroll_ag_list = tkinter.Scrollbar(ags_sel_cuadro, orient = VERTICAL)
scroll_ag_list.grid(row = 1, column = 5)
lista_ag_list = tkinter.Listbox(ags_sel_cuadro, width = 20, height = 10, yscrollcommand=scroll_ag_list.set)
lista_ag_list.grid(row = 1 , column = 4, padx = 5)
scroll_ag_list.config(command = lista_ag_list.yview)

lista_ag_list.bind('<Double-Button>', agregar_ag_dblclick)

#LISTA DE AEROS SELECCIONADOS
ag_sel_lbl = tkinter.Label(ags_sel_cuadro, text = "AGs seleccionados").grid(row = 0, column = 7, pady = 5, padx = 2)
scroll_ag_sel = tkinter.Scrollbar(ags_sel_cuadro, orient = VERTICAL)
scroll_ag_sel.grid(row = 1, column = 8)
lista_ag_sel = tkinter.Listbox(ags_sel_cuadro, width = 20, height = 10, yscrollcommand = scroll_ag_sel.set)
lista_ag_sel.grid(row = 1, column = 7, padx = 5)
scroll_ag_sel.config(command = lista_ag_sel.yview)

#agregar y quitar AGs del listado
btn_add_ag = tkinter.Button(ags_sel_cuadro, text = "Agregar", command = agregar_ag).grid(row = 2, column = 4, padx = 2, sticky = W)
btn_quit_ag = tkinter.Button(ags_sel_cuadro, text = "Quitar", command = quitar_ag).grid(row = 2, column = 4, padx = 2, sticky = E)
btn_add_all = tkinter.Button(ags_sel_cuadro, text = "Agregar todos los AGs", command = agregar_todos).grid(row = 3, column = 4, pady = 2, sticky = W + E)
#btn_quit_all = tkinter.Button(ags_sel_cuadro, text = "Quitar todos").grid(row = 3, column = 7, pady = 2, sticky = E)
btn_crear_atributos = tkinter.Button(ags_sel_cuadro, text = "Replicar variables", state = DISABLED, command = cargar_datos_ags)
btn_crear_atributos.grid(row = 2, column = 7, padx = 5, pady = 5, rowspan = 2, sticky = W + E + N + S)

##############################################################################
######################### SET DE DATOS PREDEFINIDOS ##########################
##############################################################################
# variables
Parques = ["ARIAS","ARTILLEROS","CARACOLES","JUAN PABLO TERRA","PALOMAS","PAMPA","VALENTINES"]
AG_curva = ["AG01","AG02","AG03","AG04","AG05","AG06","AG07","AG08","AG09","AG10","AG11",
            "AG12","AG13","AG14","AG15","AG16","AG17","AG18","AG19","AG20","AG21","AG22",
            "AG23","AG24","AG25","AG26","AG27","AG28","AG29","AG30","AG31","AG32","AG33",
            "AG34","AG35","AG36","AG37","AG38","AG39","AG40","AG41","AG42","AG43","AG44",
            "AG45","AG46","AG47","AG48","AG49","AG50","AG51","AG52","AG53","AG54","AG55",
            "AG56","AG57","AG58","AG59"]

# variables de combobox
parque_adme = StringVar(); parque_adme.set("")
parque_cdp = StringVar(); parque_cdp.set("")
ag_cdp = StringVar(); ag_cdp.set("")

sdp_frame = tkinter.LabelFrame(main_cuadro)
sdp_frame.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = N + E + S)
# cuadro de set de datos
sdp_frame2 = tkinter.LabelFrame(sdp_frame, text = "Set de Datos Predefinidos")
sdp_frame2.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + S)
# cuadro de datos adme
sdp_adme = tkinter.LabelFrame(sdp_frame2, text = "Datos ADME")
sdp_adme.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + S)
# seleccionar parque
sdp_lbl_adme = tkinter.Label(sdp_adme, text = "Parque")
sdp_lbl_adme.grid(row = 0, column = 0, padx = 5, pady = 5)
sdp_parque = ttk.Combobox(sdp_adme, textvariable = parque_adme, values = Parques, state = "readonly", width = 30).grid(row = 1, column = 0, pady = 3, padx = 5)
# var1 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[0], state = 'readonly', width = 50).grid(row = 0, column = 0, pady = 3, padx = 5)

# cuadros datos curva de potencia
sdp_power = tkinter.LabelFrame(sdp_frame2, text = "Datos para Curva de Potencia")
sdp_power.grid(row = 0, column = 1, padx = 5, pady = 5)
sdp_lbl_power = tkinter.Label(sdp_power, text = "Parque")
sdp_lbl_power.grid(row = 0, column = 0, padx = 5, pady = 5)
sdp_parque_2 = ttk.Combobox(sdp_power, values = Parques, state = "readonly",textvariable=parque_cdp, width = 30).grid(row = 2, column = 0, pady = 5, padx = 5)
sdp_lbl_power2 = tkinter.Label(sdp_power, text = "Aerogenerador")
sdp_lbl_power2.grid(row = 3, column = 0, padx = 5, pady = 5)
sdp_aeros = ttk.Combobox(sdp_power,values=AG_curva,state="readonly",textvariable=ag_cdp,width=30).grid(row = 4, column = 0, pady = 3, padx = 5)

# botones de cargar
sdp_cargar_adme = tkinter.Button(sdp_adme, text = "Cargar datos ADME", command = levantar_datos_adme).grid(row = 3, column = 0, padx = 5, pady = 5, sticky = W + E, ipady=3)
sdp_cargar_power = tkinter.Button(sdp_power,text = "Cargar datos CdP", command = levantar_datos_cdp).grid(row = 5, column = 0, padx = 5, pady = 5, sticky = W + E)

##############################################################################
######################### INTERFAZ GRAFICA FILTROS ###########################
##############################################################################
filter_frame = tkinter.LabelFrame(filtrados)
filter_frame.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = E)

# logo2 = tkinter.Label(filter_frame, text = 'piQuery')
# logo2.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = S + E)
# logo2.config(fg = 'black', font = ('Bahnschrift SemiLight Condensed',30))
# # etiqueta logo
# info_logo2 = tkinter.Label(filter_frame, text = 'Interfaz de consulta de datos PI')
# info_logo2.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = S + E)
# info_logo2.config(fg = 'black', font = ('Bahnschrift SemiLight Condensed',25))                                                                                           
                                                                                         
#cuadro de orden principal
encuadre_principal = tkinter.LabelFrame(filter_frame, text = "Cuadros")
encuadre_principal.grid(row = 0, column = 0, pady = 5, padx = 5)

#cuadro de variables
cuadro_variables = tkinter.LabelFrame(encuadre_principal, text = 'Seleccion de variables')
cuadro_variables.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = N + S + E + W)

#cuadro de filtros
cuadro_filtros = tkinter.LabelFrame(encuadre_principal, text = 'Filtrado de datos')
cuadro_filtros.grid(row = 0, column = 2, pady = 5, padx = 5, sticky = N + S)

#etiquetas de filtros simples
tkinter.Label(cuadro_variables).grid(row = 0, column = 0, pady = 5, padx = 1)
tkinter.Label(cuadro_variables, text = 'Seleccione variable a filtrar').grid(row = 1, column = 0, pady = 5, padx = 1)
tkinter.Label(cuadro_filtros, text = 'Valor reemplazo').grid(row = 1, column = 1, pady = 5, padx = 1)
tkinter.Label(cuadro_filtros, text = 'Datos paralizados').grid(row = 0, column = 2, pady = 5, padx = 5)
tkinter.Label(cuadro_filtros, text = 'Valores').grid(row = 1, column = 2, pady = 5, padx = 15, sticky = W)
tkinter.Label(cuadro_filtros, text = 'Pendientes').grid(row = 1, column = 2, pady = 5, padx = 15, sticky = E)
tkinter.Label(cuadro_filtros, text = 'Condicionales').grid(row = 1, column = 3, pady = 5, padx = 1)
tkinter.Label(cuadro_filtros, text = 'Acción').grid(row = 1, column = 4, pady = 5, padx = 1)

# variables de texto
string_filtrado = StringVar() # variables para escribir texto en ventana
string_filtrado.set('')
string_filtrado_label = tkinter.Label(cuadro, textvariable = string_filtrado, fg = 'red').grid(row = 5, column = 0, columnspan = 5, sticky = W + E)

#cuadro de seleccion de variable
encuadre_1 = tkinter.LabelFrame(cuadro_variables)
encuadre_1.grid(row = 2, column = 0, pady = 1, padx = 1, sticky = W + E)
#cuadro datos consecutivos
encuadre_2 = tkinter.LabelFrame(cuadro_filtros)
encuadre_2.grid(row = 2, column = 1, pady = 1, padx = 1, sticky = W + E)
#cuadro filtro condicionales 1
encuadre_3 = tkinter.LabelFrame(cuadro_filtros)
encuadre_3.grid(row = 2, column = 2, pady = 1, padx = 1, sticky = W + E)
#cuadro filtro condicionales 2
encuadre_4 = tkinter.LabelFrame(cuadro_filtros)
encuadre_4.grid(row = 2, column = 3, pady = 1, padx = 1, sticky = W + E)
#cuadro accion
encuadre_5 = tkinter.LabelFrame(cuadro_filtros)
encuadre_5.grid(row = 2, column = 4, pady = 1, padx = 1, sticky = W + E)

#arreglo de StringVar para comboboxes de variables principal
combo = list("000000000000000")
for posicion in range(0,15):
    combo[posicion] = StringVar(); combo[posicion].set('')
    #print(combo[posicion].get())
    
#menus desplegables para seleccion de variables
var1 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[0], state = 'readonly', width = 50).grid(row = 0, column = 0, pady = 3, padx = 5)
var2 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[1], state = 'readonly', width = 50).grid(row = 1, column = 0, pady = 3, padx = 5)
var3 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[2], state = 'readonly', width = 50).grid(row = 2, column = 0, pady = 3, padx = 5)
var4 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[3], state = 'readonly', width = 50).grid(row = 3, column = 0, pady = 3, padx = 5)
var5 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[4], state = 'readonly', width = 50).grid(row = 4, column = 0, pady = 3, padx = 5)
var6 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[5], state = 'readonly', width = 50).grid(row = 5, column = 0, pady = 3, padx = 5)
var7 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[6], state = 'readonly', width = 50).grid(row = 6, column = 0, pady = 3, padx = 5)
var8 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[7], state = 'readonly', width = 50).grid(row = 7, column = 0, pady = 3, padx = 5)
var9 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[8], state = 'readonly', width = 50).grid(row = 8, column = 0, pady = 3, padx = 5)
var10 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[9], state = 'readonly', width = 50).grid(row = 9, column = 0, pady = 3, padx = 5)
var11 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[10], state = 'readonly', width = 50).grid(row = 10, column = 0, pady = 3, padx = 5)
var12 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[11], state = 'readonly', width = 50).grid(row = 11, column = 0, pady = 3, padx = 5)
var13 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[12], state = 'readonly', width = 50).grid(row = 12, column = 0, pady = 3, padx = 5)
var14 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[13], state = 'readonly', width = 50).grid(row = 13, column = 0, pady = 3, padx = 5)
var15 = ttk.Combobox(encuadre_1, values = menu_variables, textvariable = combo[14], state = 'readonly', width = 50).grid(row = 14, column = 0, pady = 3, padx = 5)
 
# ventana_filtros.bind('<<ComboboxSelected>>', callback_function)
ventana.bind('<<ComboboxSelected>>', callback_function)
                    
#arreglo de StringVar para entrys de señal para reemplazar
replace = list("123456789123456")
for posicion in range(0,15):
    replace[posicion] = StringVar(); replace[posicion].set('')
    #print(replace[posicion].get())

#entrys senal para reemplazar                                                    
senal1 = ttk.Entry(encuadre_2, textvariable = replace[0], width = 15).grid(row = 0, column = 1, pady = 3, padx = 5)                                                    
senal2 = ttk.Entry(encuadre_2, textvariable = replace[1], width = 15).grid(row = 1, column = 1, pady = 3, padx = 5)
senal3 = ttk.Entry(encuadre_2, textvariable = replace[2], width = 15).grid(row = 2, column = 1, pady = 3, padx = 5)
senal4 = ttk.Entry(encuadre_2, textvariable = replace[3], width = 15).grid(row = 3, column = 1, pady = 3, padx = 5)
senal5 = ttk.Entry(encuadre_2, textvariable = replace[4], width = 15).grid(row = 4, column = 1, pady = 3, padx = 5)
senal6 = ttk.Entry(encuadre_2, textvariable = replace[5], width = 15).grid(row = 5, column = 1, pady = 3, padx = 5)
senal7 = ttk.Entry(encuadre_2, textvariable = replace[6], width = 15).grid(row = 6, column = 1, pady = 3, padx = 5)
senal8 = ttk.Entry(encuadre_2, textvariable = replace[7], width = 15).grid(row = 7, column = 1, pady = 3, padx = 5)
senal9 = ttk.Entry(encuadre_2, textvariable = replace[8], width = 15).grid(row = 8, column = 1, pady = 3, padx = 5)
senal10 = ttk.Entry(encuadre_2, textvariable = replace[9], width = 15).grid(row = 9, column = 1, pady = 3, padx = 5)
senal11 = ttk.Entry(encuadre_2, textvariable = replace[10], width = 15).grid(row = 10, column = 1, pady = 3, padx = 5)
senal12 = ttk.Entry(encuadre_2, textvariable = replace[11], width = 15).grid(row = 11, column = 1, pady = 3, padx = 5)
senal13 = ttk.Entry(encuadre_2, textvariable = replace[12], width = 15).grid(row = 12, column = 1, pady = 3, padx = 5)
senal14 = ttk.Entry(encuadre_2, textvariable = replace[13], width = 15).grid(row = 13, column = 1, pady = 3, padx = 5)
senal15 = ttk.Entry(encuadre_2, textvariable = replace[14], width = 15).grid(row = 14, column = 1, pady = 3, padx = 5)
                                                     
#DATOS PARALIZADOS     

#arreglo de StringVar que define el valor de la cantidad de datos consecutivos
consecutivo_ = list("123456789123456")
for posicion in range(0,15):
    consecutivo_[posicion] = StringVar(); #consecutivo_[posicion].set('3')
    #print(consecutivo_[posicion].get())

#valores consecutivos                          
valor_consecutivo1 = ttk.Entry(encuadre_3, textvariable = consecutivo_[0], width = 5).grid(row = 0, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo2 = ttk.Entry(encuadre_3, textvariable = consecutivo_[1], width = 5).grid(row = 1, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo3 = ttk.Entry(encuadre_3, textvariable = consecutivo_[2], width = 5).grid(row = 2, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo4 = ttk.Entry(encuadre_3, textvariable = consecutivo_[3], width = 5).grid(row = 3, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo5 = ttk.Entry(encuadre_3, textvariable = consecutivo_[4], width = 5).grid(row = 4, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo6 = ttk.Entry(encuadre_3, textvariable = consecutivo_[5], width = 5).grid(row = 5, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo7 = ttk.Entry(encuadre_3, textvariable = consecutivo_[6], width = 5).grid(row = 6, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo8 = ttk.Entry(encuadre_3, textvariable = consecutivo_[7], width = 5).grid(row = 7, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo9 = ttk.Entry(encuadre_3, textvariable = consecutivo_[8], width = 5).grid(row = 8, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo10 = ttk.Entry(encuadre_3, textvariable = consecutivo_[9], width = 5).grid(row = 9, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo11 = ttk.Entry(encuadre_3, textvariable = consecutivo_[10], width = 5).grid(row = 10, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo12 = ttk.Entry(encuadre_3, textvariable = consecutivo_[11], width = 5).grid(row = 11, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo13 = ttk.Entry(encuadre_3, textvariable = consecutivo_[12], width = 5).grid(row = 12, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo14 = ttk.Entry(encuadre_3, textvariable = consecutivo_[13], width = 5).grid(row = 13, column = 1, pady = 3, padx = 15, sticky = W)   
valor_consecutivo15 = ttk.Entry(encuadre_3, textvariable = consecutivo_[14], width = 5).grid(row = 14, column = 1, pady = 3, padx = 15, sticky = W)   

#variables para valores consecutivos
#arreglo de StringVar que define el valor de la cantidad de pendientes consecutivas
pendiente_ = list("123456789123456")
for posicion in range(0,15):
    pendiente_[posicion] = StringVar(); #pendiente_[posicion].set('2')
    #print(pendiente_[posicion].get())

#pendientes consecutivas                                 
pendiente_consecutivo1 = ttk.Entry(encuadre_3, textvariable = pendiente_[0], width = 5).grid(row = 0, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo2 = ttk.Entry(encuadre_3, textvariable = pendiente_[1], width = 5).grid(row = 1, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo3 = ttk.Entry(encuadre_3, textvariable = pendiente_[2], width = 5).grid(row = 2, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo4 = ttk.Entry(encuadre_3, textvariable = pendiente_[3], width = 5).grid(row = 3, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo5 = ttk.Entry(encuadre_3, textvariable = pendiente_[4], width = 5).grid(row = 4, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo6 = ttk.Entry(encuadre_3, textvariable = pendiente_[5], width = 5).grid(row = 5, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo7 = ttk.Entry(encuadre_3, textvariable = pendiente_[6], width = 5).grid(row = 6, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo8 = ttk.Entry(encuadre_3, textvariable = pendiente_[7], width = 5).grid(row = 7, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo9 = ttk.Entry(encuadre_3, textvariable = pendiente_[8], width = 5).grid(row = 8, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo10 = ttk.Entry(encuadre_3, textvariable = pendiente_[9], width = 5).grid(row = 9, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo11 = ttk.Entry(encuadre_3, textvariable = pendiente_[10], width = 5).grid(row = 10, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo12 = ttk.Entry(encuadre_3, textvariable = pendiente_[11], width = 5).grid(row = 11, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo13 = ttk.Entry(encuadre_3, textvariable = pendiente_[12], width = 5).grid(row = 12, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo14 = ttk.Entry(encuadre_3, textvariable = pendiente_[13], width = 5).grid(row = 13, column = 4, pady = 3, padx = 15, sticky = E) 
pendiente_consecutivo15 = ttk.Entry(encuadre_3, textvariable = pendiente_[14], width = 5).grid(row = 14, column = 4, pady = 3, padx = 15, sticky = E) 

#arreglo de StringVar para comboboxes de variables secudaria
combo2 = list("123456789123456")
for posicion in range(0,15):
    combo2[posicion] = StringVar(); combo2[posicion].set('')
    #print(combo2[posicion].get())
    
#segunda variable
segunda_var1 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[0], state = 'readonly', width = 50).grid(row = 0, column = 0, pady = 3, padx = 5)
segunda_var2 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[1], state = 'readonly', width = 50).grid(row = 1, column = 0, pady = 3, padx = 5)
segunda_var3 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[2], state = 'readonly', width = 50).grid(row = 2, column = 0, pady = 3, padx = 5)
segunda_var4 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[3], state = 'readonly', width = 50).grid(row = 3, column = 0, pady = 3, padx = 5)
segunda_var5 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[4], state = 'readonly', width = 50).grid(row = 4, column = 0, pady = 3, padx = 5)
segunda_var6 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[5], state = 'readonly', width = 50).grid(row = 5, column = 0, pady = 3, padx = 5)
segunda_var7 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[6], state = 'readonly', width = 50).grid(row = 6, column = 0, pady = 3, padx = 5)
segunda_var8 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[7], state = 'readonly', width = 50).grid(row = 7, column = 0, pady = 3, padx = 5)
segunda_var9 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[8], state = 'readonly', width = 50).grid(row = 8, column = 0, pady = 3, padx = 5)
segunda_var10 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[9], state = 'readonly', width = 50).grid(row = 9, column = 0, pady = 3, padx = 5)
segunda_var11 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[10], state = 'readonly', width = 50).grid(row = 10, column = 0, pady = 3, padx = 5)
segunda_var12 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[11], state = 'readonly', width = 50).grid(row = 11, column = 0, pady = 3, padx = 5)
segunda_var13 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[12], state = 'readonly', width = 50).grid(row = 12, column = 0, pady = 3, padx = 5)
segunda_var14 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[13], state = 'readonly', width = 50).grid(row = 13, column = 0, pady = 3, padx = 5)
segunda_var15 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[14], state = 'readonly', width = 50).grid(row = 14, column = 0, pady = 3, padx = 5)

#arreglo de StringVar para comboboxes de comparadores lógicos
comparador = list("123456789123456")
for posicion in range(0,15):
    comparador[posicion] = StringVar(); comparador[posicion].set('')
    #print(comparador[posicion].get())

#comparador lógico
comparador1 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[0], state = 'readonly', width = 7).grid(row = 0, column = 1, pady = 3, padx = 5)
comparador2 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[1], state = 'readonly', width = 7).grid(row = 1, column = 1, pady = 3, padx = 5)
comparador3 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[2], state = 'readonly', width = 7).grid(row = 2, column = 1, pady = 3, padx = 5)
comparador4 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[3], state = 'readonly', width = 7).grid(row = 3, column = 1, pady = 3, padx = 5)
comparador5 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[4], state = 'readonly', width = 7).grid(row = 4, column = 1, pady = 3, padx = 5)
comparador6 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[5], state = 'readonly', width = 7).grid(row = 5, column = 1, pady = 3, padx = 5)
comparador7 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[6], state = 'readonly', width = 7).grid(row = 6, column = 1, pady = 3, padx = 5)
comparador8 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[7], state = 'readonly', width = 7).grid(row = 7, column = 1, pady = 3, padx = 5)
comparador9 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[8], state = 'readonly', width = 7).grid(row = 8, column = 1, pady = 3, padx = 5)
comparador10 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[9], state = 'readonly', width = 7).grid(row = 9, column = 1, pady = 3, padx = 5)
comparador11 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[10], state = 'readonly', width = 7).grid(row = 10, column = 1, pady = 3, padx = 5)
comparador12 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[11], state = 'readonly', width = 7).grid(row = 11, column = 1, pady = 3, padx = 5)
comparador13 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[12], state = 'readonly', width = 7).grid(row = 12, column = 1, pady = 3, padx = 5)
comparador14 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[13], state = 'readonly', width = 7).grid(row = 13, column = 1, pady = 3, padx = 5)
comparador15 = ttk.Combobox(encuadre_4, values = condiciones, textvariable = comparador[14], state = 'readonly', width = 7).grid(row = 14, column = 1, pady = 3, padx = 5)

#arreglo de StringVar para comboboxes de valor de comparación lógica
compare_value = list("123456789123456")
for posicion in range(0,15):
    compare_value[posicion] = StringVar(); compare_value[posicion].set('')
   # print(compare_value[posicion].get())
    
#señal
segunda_senal1 = ttk.Entry(encuadre_4, textvariable = compare_value[0], width = 10).grid(row = 0, column = 2, pady = 3, padx = 5) 
segunda_senal2 = ttk.Entry(encuadre_4, textvariable = compare_value[1], width = 10).grid(row = 1, column = 2, pady = 3, padx = 5) 
segunda_senal3 = ttk.Entry(encuadre_4, textvariable = compare_value[2], width = 10).grid(row = 2, column = 2, pady = 3, padx = 5) 
segunda_senal4 = ttk.Entry(encuadre_4, textvariable = compare_value[3], width = 10).grid(row = 3, column = 2, pady = 3, padx = 5) 
segunda_senal5 = ttk.Entry(encuadre_4, textvariable = compare_value[4], width = 10).grid(row = 4, column = 2, pady = 3, padx = 5) 
segunda_senal6 = ttk.Entry(encuadre_4, textvariable = compare_value[5], width = 10).grid(row = 5, column = 2, pady = 3, padx = 5) 
segunda_senal7 = ttk.Entry(encuadre_4, textvariable = compare_value[6], width = 10).grid(row = 6, column = 2, pady = 3, padx = 5) 
segunda_senal8 = ttk.Entry(encuadre_4, textvariable = compare_value[7], width = 10).grid(row = 7, column = 2, pady = 3, padx = 5) 
segunda_senal9 = ttk.Entry(encuadre_4, textvariable = compare_value[8], width = 10).grid(row = 8, column = 2, pady = 3, padx = 5) 
segunda_senal10 = ttk.Entry(encuadre_4, textvariable = compare_value[9], width = 10).grid(row = 9, column = 2, pady = 3, padx = 5) 
segunda_senal11 = ttk.Entry(encuadre_4, textvariable = compare_value[10], width = 10).grid(row = 10, column = 2, pady = 3, padx = 5) 
segunda_senal12 = ttk.Entry(encuadre_4, textvariable = compare_value[11], width = 10).grid(row = 11, column = 2, pady = 3, padx = 5) 
segunda_senal13 = ttk.Entry(encuadre_4, textvariable = compare_value[12], width = 10).grid(row = 12, column = 2, pady = 3, padx = 5) 
segunda_senal14 = ttk.Entry(encuadre_4, textvariable = compare_value[13], width = 10).grid(row = 13, column = 2, pady = 3, padx = 5) 
segunda_senal15 = ttk.Entry(encuadre_4, textvariable = compare_value[14], width = 10).grid(row = 14, column = 2, pady = 3, padx = 5) 

#arreglo de StringVar para comboboxes de acción a realizar
accion_ = list("123456789123456")
for posicion in range(0,15):
    accion_[posicion] = StringVar(); accion_[posicion].set('')
    #print(accion_[posicion].get())

#ACCION
accion1 = ttk.Combobox(encuadre_5, textvariable = accion_[0], values = accion, state = 'readonly', width = 20).grid(row = 0, column = 0, pady = 3, padx = 5)
accion2 = ttk.Combobox(encuadre_5, textvariable = accion_[1], values = accion, state = 'readonly', width = 20).grid(row = 1, column = 0, pady = 3, padx = 5)
accion3 = ttk.Combobox(encuadre_5, textvariable = accion_[2], values = accion, state = 'readonly', width = 20).grid(row = 2, column = 0, pady = 3, padx = 5)
accion4 = ttk.Combobox(encuadre_5, textvariable = accion_[3], values = accion, state = 'readonly', width = 20).grid(row = 3, column = 0, pady = 3, padx = 5)
accion5 = ttk.Combobox(encuadre_5, textvariable = accion_[4], values = accion, state = 'readonly', width = 20).grid(row = 4, column = 0, pady = 3, padx = 5)
accion6 = ttk.Combobox(encuadre_5, textvariable = accion_[5], values = accion, state = 'readonly', width = 20).grid(row = 5, column = 0, pady = 3, padx = 5)
accion7 = ttk.Combobox(encuadre_5, textvariable = accion_[6], values = accion, state = 'readonly', width = 20).grid(row = 6, column = 0, pady = 3, padx = 5)
accion8 = ttk.Combobox(encuadre_5, textvariable = accion_[7], values = accion, state = 'readonly', width = 20).grid(row = 7, column = 0, pady = 3, padx = 5)
accion9 = ttk.Combobox(encuadre_5, textvariable = accion_[8], values = accion, state = 'readonly', width = 20).grid(row = 8, column = 0, pady = 3, padx = 5)
accion10 = ttk.Combobox(encuadre_5, textvariable = accion_[9], values = accion, state = 'readonly', width = 20).grid(row = 9, column = 0, pady = 3, padx = 5)
accion11 = ttk.Combobox(encuadre_5, textvariable = accion_[10], values = accion, state = 'readonly', width = 20).grid(row = 10, column = 0, pady = 3, padx = 5)
accion12 = ttk.Combobox(encuadre_5, textvariable = accion_[11], values = accion, state = 'readonly', width = 20).grid(row = 11, column = 0, pady = 3, padx = 5)
accion13 = ttk.Combobox(encuadre_5, textvariable = accion_[12], values = accion, state = 'readonly', width = 20).grid(row = 12, column = 0, pady = 3, padx = 5)
accion14 = ttk.Combobox(encuadre_5, textvariable = accion_[13], values = accion, state = 'readonly', width = 20).grid(row = 13, column = 0, pady = 3, padx = 5)
accion15 = ttk.Combobox(encuadre_5, textvariable = accion_[14], values = accion, state = 'readonly', width = 20).grid(row = 14, column = 0, pady = 3, padx = 5)

# #cuadro de botones
cuadro_botones = ttk.LabelFrame(encuadre_principal, text = 'Transformar datos')
cuadro_botones.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = W + E)  

# boton para cargar en combobox las variables a filatrar
# refresh_btn = ttk.Button(cuadro_botones, text = "Cargar/Actualizar datos", command = refresh)
# refresh_btn.grid(row = 0, column = 1, columnspan = 2, pady = 5, padx = 5, sticky = W + E)
 
#aplicar filtros
aplicar = ttk.Button(cuadro_botones, text = 'Aplicar filtros', command = aplicar_filtros)
# aplicar = ttk.Button(cuadro_botones, text = 'Aplicar', command = filtrar_todos)
aplicar.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W + E)

# filtrar_todos

#exportar archivos con datos filtrados
exportar_csv = ttk.Button(cuadro_botones, text = "Exportar", state = DISABLED, command = exportar_filtrados)
exportar_csv.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = W + E)

# transformar todos los datos filtrados en huecos
aplicar_huecos = ttk.Button(cuadro_botones, text = "Aplicar huecos en datos filtrados", state = DISABLED, command = aplicar_huecos_en_filtrados)
aplicar_huecos.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = W + E)

# boton para eliminar todos los filtros seleccionados
eliminar_filtros = ttk.Button(cuadro_botones, text = 'Eliminar todos los filtros seleccionados', state = DISABLED, command = eliminar_filtros_aplicados)
eliminar_filtros.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = W + E)

#######################################################################
###################### ANALISIS GRAFICO ###############################
#######################################################################
#  # cuadro principal
# grf_cuadro_principal = ttk.LabelFrame(graficar)
# grf_cuadro_principal.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = E)
# # cuadro secundario
# grf_cuadro_2 = ttk.LabelFrame(grf_cuadro_principal, text = "Selección de Parámetros")
# grf_cuadro_2.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = N + S)
# # cuandro cuadro de gráficos
# grf_cuadro_graf = ttk.LabelFrame(grf_cuadro_principal, text = "Gráficos")
# # cuadro de variables
# grf_cuadro_variables = ttk.LabelFrame(grf_cuadro_2, text = "Variables")
# grf_cuadro_variables.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = N + S)
# # cuadro de opciones
# grf_cuadro_tipos = ttk.LabelFrame(grf_cuadro_2, text = "Tipo de Análisis")
# grf_cuadro_tipos.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = N + S)

# # boton para actualizar variables a graficar
# grf_btn_cargar = ttk.Button(graficar, text = "Cargar/Actalizar", command = actualizar_ventana_grafica)
# grf_btn_cargar.grid(row = 1, column = 0, padx = 5, pady = 5)

# # creo vector de variables a graficar
# variables_graficar = datos.columns

# # variables para checkbox
# checkbox_variables = []
# checkVar = []
# chosen = []
# for i in range(0,len(variables_graficar)):
#     checkbox_variables.append(variables_graficar[i])
#     checkVar.append(tkinter.IntVar())
#     chosen.append("object")

# # checks para seleccion de variables
# for var in range(1,len(variables_graficar)):
#     checkbox_variables[var] = tkinter.Checkbutton(grf_cuadro_variables, variable = checkVar[var], command = check_clicked,
#                                                   text = variables_graficar[var]).grid(row = var, column = 0, 
#                                                       pady = 5, padx = 5, sticky = W)
# # chosen                                                                                       
# for var in range(1,len(variables_graficar)):
#     chosen[var] = checkVar[var].get() in ("on", "off")

# # botones de acciones
# # evolucion temporal
# boton_evol_temp = tkinter.Button(grf_cuadro_tipos, text = "Evolución temporal", command = evolucion_temporal)
# boton_evol_temp.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = W + E)
# # histogramas
# boton_histograma = tkinter.Button(grf_cuadro_tipos, text = "Histograma", command = histograma)
# boton_histograma.grid(row = 1, column = 0, pady = 5, padx = 5, sticky = W + E)
# # regresion lineal
# boton_regresion = tkinter.Button(grf_cuadro_tipos, text = "Regresión lineal")
# boton_regresion.grid(row = 2, column = 0, pady = 5, padx = 5, sticky = W + E)
# # promedios mensuales
# boton_promedios = tkinter.Button(grf_cuadro_tipos, text = "Promedios mensuales")
# boton_promedios.grid(row = 3, column = 0, pady = 5, padx = 5, sticky = W + E)
# # disponibilidad de datos
# boton_disponibilidad = tkinter.Button(grf_cuadro_tipos, text = "Disponibilidad de datos")
# boton_disponibilidad.grid(row = 4, column = 0, pady = 5, padx = 5, sticky = W + E)


# agregar pestaña creada
nb.add(consulta,text = "Consulta de Datos") # linea 917
nb.add(filtrados,text = "Validación de Datos")
# nb.add(graficar,text= "Análisis gráfico")

#funcion de actualizacion de listas, muy muy importante para que esto ande
actualizar_listado(listado_actual, lista_elementos)

ventana.mainloop()
#valentineseolico2018


# 2021-02-05 12:40:00
# 2021-02-05 13:40:00