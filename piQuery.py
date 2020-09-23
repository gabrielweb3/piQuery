#librerias tkinter
import tkinter
from tkinter import *
from tkinter import ttk

#librerias PI
import sys  
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')  
import clr  
clr.AddReference('OSIsoft.AFSDK')  

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
from matplotlib.dates import date2num
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.dates import bytespdate2num
from datetime import datetime
from matplotlib import dates as mpl_dates
import math

# #funciones 
# from obterner_elementos import obterner_elementos 
# from obtener_atributos import obtener_atributos
# from transformar_coleccion_AF import transformar_coleccion_AF
# from borrar_listado import borrar_listado
# from mostrar_item import mostrar_item
# from actualizar_listado import actualizar_listado
# from avanzar import avanzar
# from retroceder import retroceder
# from avanzar_dblclick import avanzar_dblclick
# from agregar_seleccion import agregar_seleccion
# from quitar_seleccion import quitar_seleccion
# from lista_variables import lista_variables
# from lista_ags import lista_ags
# from agregar_ag import agregar_ag
# from agregar_ag_dblclick import agregar_ag_dblclick
# from quitar_ag import quitar_ag
# from agregar_todos import agregar_todos
# from cargarDatos import cargarDatos
# from exportar import exportar


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
        print(int(item[0]))
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
    global atributos_seleccionados
    global ag_actual
    global aerogens
    aux = 0           
    if len(ruta)>=4:
        ag_actual.set(ruta[3])
        aerogens.append(ruta[3])
    else:
        ag_actual.set(" - ")
    for var in atributos_seleccionados:
        #variables.append(atributos_seleccionados[aux])
        lista_var_selected.insert(END,atributos_seleccionados[aux])
        aux+=1

#mostrar listado de aerogeneradores en un listbox
def lista_ags():
    global ruta
    aux = 0
    aeros = obtener_elementos(ruta[2])
    listado_ags = transformar_coleccion_AF(aeros)
    for var in listado_ags:
        lista_ag_list.insert(END, listado_ags[aux])
        aux+=1
        
#agregar ag a lista de seleccionados
def agregar_ag():
    global ruta
    global aerogens
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
    aux = 0
    aeros = obtener_elementos(ruta[2])
    listado_ags = transformar_coleccion_AF(aeros)
    for var in listado_ags:
        lista_ag_sel.insert(END, listado_ags[aux])
        aerogens.append(listado_ags[aux])
        aux+=1 


#CONSULTA DE DATOS
#esta funcion se encarga de conectar con el servidor y traer todos los datos
#solicitados entre las fechas que se le diga
def cargarDatos():      
    #Periodo  
    fecha_inicio = fecha_ini_var.get()
    fecha_fin = fecha_fin_var.get()
    
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
    for senal in signals:    
        #atributos_PI.append(senal.Data)
        #atributos_PI.append(PIPoint.FindPIPoint(piServer, senal))
        atributos_PI.append(senal.PIPoint)
        
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
    for consulta in atributos_PI:
        #Guardo el nombre del elemento que estoy consultando
        #nombre_element = ruta[3]
        #nombre_atribut = consulta.Name
        
        #nombro el atributo con el nombre del ag y la variable seleccionada
        #nombre_atributo = str(nombre_element)+str(" - ")+str(nombre_atribut)
        #nombre_atributo = consulta.Attribute
        nombre_atributo = consulta.Name
        
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
        #DATA
        #resultado = consulta.RecordedValues(timerange, AFBoundaryType.Inside,None,"", False)
        #PIPOINT
        resultado = consulta.RecordedValues(timerange, AFBoundaryType.Inside, "", False)
    
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
            
        nombre_columna2=nombre_atributo
        df_aux1=pd.DataFrame({nombre_columna2:datos},index=indice)
        df=pd.concat([df,df_aux1], axis=1, sort=False)
        
        #convertir dataframe a valores numericos
        #cuando el contenido no es numerico pone un NaN en su lugar
        df_2 = df.apply(pd.to_numeric,errors='coerce')
        #cuando hago esta conversion tambien convierte el vector de fechas a numerico
        #por lo tanto tengo que volver el vector de fechas a su estado original
        df_2['fecha'] = df['fecha']
        
        #luego de que df_2 queda con el la columna de fechas correcta, lo vuelvo a convertir en df
        df = df_2
        
        #con esto todos los valores no numericos del dataframe seran NaN
        #por lo tanto ahora puedo aplicar el filtro de valores NaN

        #DOBLE FILTRO NAN
        #filtro de valores nan, en caso de que detecte un valor nan lo reemplaza
        #...con un string vacio
        for col in range(1,len(df.columns)):
            for fila in range(0,len(df.iloc[:,0])):
                if math.isnan(df.iloc[fila,col]):
                    df.iloc[fila,col] = ""
                    

        #reemplaza todos los datos nan/nad/nat con huecos(formato string, ojo con esto, probar si no trae problemas)
        df = df.fillna('')
        
        #elimino primera columa inecesaria con indices
        #del df[df.columns[0]]

    global estado_txt
    estado_txt.set("Se cargan los datos satisfactoriamente")
    #global variables
    #variables.set(df.columns)
    
    #habilito botones inicialmente deshabilitados 
    btn_crear_atributos.config(state = NORMAL)
    cargar_datos_aeros.config(state = NORMAL)
    refresh_button.config(state = NORMAL)
    exporta_datos.config(state = NORMAL)
    filtros_btn.config(state = NORMAL)
                               
#EXPORTAR DATOS A CSV
#esta funcion se encarga de escribir los datos almacenados en el dataframe df
#y exportarlos a un archivo csv
def exportarDatos():
    
    df.to_csv(str(ruta[1])+'_datos_exportados.csv')
    global estado_txt
    estado_txt.set(time.strftime("%H:%M - ") + "Se exportan los datos satisfactoriamente")
    #df = []

#filtro de datos consecutivos    
def datos_consecutivos():

    global df    
    global consecutivos
    #ingreso cantidad de datos consecutivos a filtrar
    con_dat = consecutivos.get()
    consecutives = int(con_dat)
    
    #dataframe testigo de valores repetidos
    testigo = df
    
    #analisis de columnas buscando repetidos consecutivos
    for col in range(0,len(df.columns)):
        
        #agrupo los datos consecutivos igual o mayor, en este caso, a 3
        #se van a eliminar todos los datos repetidos consecutivos
        #filtrados = testigo.groupby((testigo.iloc[:,col].shift() != testigo.iloc[:,col]).\
                #cumsum()).filter(lambda x: len(x) >= consecutives)
            
        filtrados = df.groupby((df.iloc[:,col].shift() != df.iloc[:,col]).\
                cumsum()).filter(lambda x: len(x) >= consecutives)
        
        #agrego una columna que me muestra 0 y 1 en caso de que los datos se repitan o no
        #cada una de estas columnas muestra 1 en caso de que un valor se haya repetido 
        #un numero x de veces en una columna del dataframe, agrega una columa boolena
        #por cada columna analizada
        testigo.iloc[:,col] = np.where(testigo.index.isin(filtrados.index),np.nan,df.iloc[:,col])
            
    #aplico filtro de nan
    df = df.fillna('')
    
    global estado_txt
    estado_txt.set("Se aplica filtro de datos consecutivos satisfactoriamente")

#funcion para crear, para cada aerogenerador seleccionado, la cantidad de atributos igual...
#...a la seleccionada para el ag original
def crear_atributos_varios_ags():
    global atributos_PI
    global aerogens
    global atributos_finales
    
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
    estado_txt.set("Se replican las variables para los aerogeneradores seleccionados")
        
        
#cargar variables seleccionadas para aerogeneradores seleccionados
def cargar_datos_ags():     
    global aerogens     
    global atribuitos_finales
    
    for ag in aerogens:
        #Periodo
        fecha_inicio = fecha_ini_var.get()
        fecha_fin = fecha_fin_var.get()
        
        #Tags
        signals = atributos_finales
        
        #Se definen variables necesarias para la consulta
        #Variable del tipo AFtimeRange con los valores de inicio y fin del periodo
        timerange = AFTimeRange(fecha_inicio, fecha_fin)
        #print(AFTimeRange(fecha_inicio, fecha_fin))
    
        #Genero los atributos para consulta
        global atributos_PI
        atributos_PI = []
        
        #Agrego los AFData correspondientes a los nombres de los Tags
        for senal in signals:    
            #atributos_PI.append(senal.PIPoint)#MIRAR ACA 
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
        for consulta in atributos_PI:
            #Guardo el nombre del elemento que estoy consultando
            nombre_atributo = consulta.Name
            
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
            resultado = consulta.RecordedValues(timerange, AFBoundaryType.Inside,None,"", False)
    
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
            
            #con esto todos los valores no numericos del dataframe seran NaN
            #por lo tanto ahora puedo aplicar el filtro de valores NaN
            #reemplaza todos los datos nan/nad/nat con huecos(formato string, ojo con esto, probar si no trae problemas)
            df = df.fillna('')
            
            #elimino primera columa inecesaria con indices
            # del df[df.columns[0]]
    
        global estado_txt
        estado_txt.set(time.strftime("%H:%M - ") + "Se exportan los datos satisfactoriamente")
        #global variables
        #variables.set(df.columns)
        
        df.to_csv(str(ruta[1])+'_datos_exportados.csv')
       
def callback_function():
    print(combo[0].get())
    
## VENTANA DE FILTROS ##
def ventana_filtros():
    
    ventana_filtros = tkinter.Toplevel(ventana)
    
    ##############################################################################
    ######################### VARIABLES GLOBALES #################################
    ##############################################################################
    #textdata.csv
    
    global atributos_seleccionados
    global df
    
    #df = pd.read_csv('textdata.csv')
    
    #variable de variables para menu desplegable
    # for columna in range(1,len(df.columns)):
    #     atributos_seleccionados.append(df.columns[columna])
        
    #opciones de menues desplegables
    condiciones = ['<', '>', '=', '!=', '<=', '>=']
    # suplantar = ['nan', 'hueco', 'otro']
    accion = ['Reemplazar', 'Reemplazar varios', 'Eliminar diezminutal']
    
    ##############################################################################
    ######################### INTERFAZ GRAFICA ###################################
    ##############################################################################
    #configuracion de ventana principal
    ventana_filtros = tkinter.Tk()
    ventana_filtros.title('Validacion de Datos')
    
    #cuadro de orden principal
    encuadre_principal = tkinter.LabelFrame(ventana_filtros)
    encuadre_principal.grid(row = 0, column = 0, pady = 5, padx = 5)
    
    #cuadro de variables
    cuadro_variables = tkinter.LabelFrame(encuadre_principal, text = 'Seleccion de variables')
    cuadro_variables.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = N + S + E + W)
    
    #cuadro de filtros
    cuadro_filtros = tkinter.LabelFrame(encuadre_principal, text = 'Filtrado de datos')
    cuadro_filtros.grid(row = 0, column = 1, pady = 5, padx = 5, sticky = N + S)
    
    #etiquetas de filtros simples
    tkinter.Label(cuadro_variables).grid(row = 0, column = 0, pady = 5, padx = 1)
    tkinter.Label(cuadro_variables, text = 'Seleccione variable a filtrar').grid(row = 1, column = 0, pady = 5, padx = 1)
    tkinter.Label(cuadro_filtros, text = 'Señal').grid(row = 1, column = 1, pady = 5, padx = 1)
    tkinter.Label(cuadro_filtros, text = 'Datos paralizados').grid(row = 0, column = 2, pady = 5, padx = 5)
    tkinter.Label(cuadro_filtros, text = 'Valores').grid(row = 1, column = 2, pady = 5, padx = 15, sticky = W)
    tkinter.Label(cuadro_filtros, text = 'Pendientes').grid(row = 1, column = 2, pady = 5, padx = 15, sticky = E)
    tkinter.Label(cuadro_filtros, text = 'Condicionales').grid(row = 1, column = 3, pady = 5, padx = 1)
    tkinter.Label(cuadro_filtros, text = 'Acción').grid(row = 1, column = 4, pady = 5, padx = 1)
    
    
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
    var1 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[0], state = 'readonly', width = 40).grid(row = 0, column = 0, pady = 3, padx = 5)
    var2 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[1], state = 'readonly', width = 40).grid(row = 1, column = 0, pady = 3, padx = 5)
    var3 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[2], state = 'readonly', width = 40).grid(row = 2, column = 0, pady = 3, padx = 5)
    var4 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[3], state = 'readonly', width = 40).grid(row = 3, column = 0, pady = 3, padx = 5)
    var5 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[4], state = 'readonly', width = 40).grid(row = 4, column = 0, pady = 3, padx = 5)
    var6 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[5], state = 'readonly', width = 40).grid(row = 5, column = 0, pady = 3, padx = 5)
    var7 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[6], state = 'readonly', width = 40).grid(row = 6, column = 0, pady = 3, padx = 5)
    var8 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[7], state = 'readonly', width = 40).grid(row = 7, column = 0, pady = 3, padx = 5)
    var9 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[8], state = 'readonly', width = 40).grid(row = 8, column = 0, pady = 3, padx = 5)
    var10 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[9], state = 'readonly', width = 40).grid(row = 9, column = 0, pady = 3, padx = 5)
    var11 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[10], state = 'readonly', width = 40).grid(row = 10, column = 0, pady = 3, padx = 5)
    var12 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[11], state = 'readonly', width = 40).grid(row = 11, column = 0, pady = 3, padx = 5)
    var13 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[12], state = 'readonly', width = 40).grid(row = 12, column = 0, pady = 3, padx = 5)
    var14 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[13], state = 'readonly', width = 40).grid(row = 13, column = 0, pady = 3, padx = 5)
    var15 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[14], state = 'readonly', width = 40).grid(row = 14, column = 0, pady = 3, padx = 5)
     
    ventana_filtros.bind('<<ComboboxSelected>>', callback_function)
                        
    #arreglo de StringVar para entrys de señal para reemplazar
    replace = list("123456789123456")
    for posicion in range(0,15):
        replace[posicion] = StringVar(); replace[posicion].set('')
        #print(replace[posicion].get())
    
    #entrys senal para reemplazar                                                    
    senal1 = ttk.Entry(encuadre_2, textvariable = replace[0], width = 10).grid(row = 0, column = 1, pady = 3, padx = 5)                                                    
    senal2 = ttk.Entry(encuadre_2, textvariable = replace[1], width = 10).grid(row = 1, column = 1, pady = 3, padx = 5)
    senal3 = ttk.Entry(encuadre_2, textvariable = replace[2], width = 10).grid(row = 2, column = 1, pady = 3, padx = 5)
    senal4 = ttk.Entry(encuadre_2, textvariable = replace[3], width = 10).grid(row = 3, column = 1, pady = 3, padx = 5)
    senal5 = ttk.Entry(encuadre_2, textvariable = replace[4], width = 10).grid(row = 4, column = 1, pady = 3, padx = 5)
    senal6 = ttk.Entry(encuadre_2, textvariable = replace[5], width = 10).grid(row = 5, column = 1, pady = 3, padx = 5)
    senal7 = ttk.Entry(encuadre_2, textvariable = replace[6], width = 10).grid(row = 6, column = 1, pady = 3, padx = 5)
    senal8 = ttk.Entry(encuadre_2, textvariable = replace[7], width = 10).grid(row = 7, column = 1, pady = 3, padx = 5)
    senal9 = ttk.Entry(encuadre_2, textvariable = replace[8], width = 10).grid(row = 8, column = 1, pady = 3, padx = 5)
    senal10 = ttk.Entry(encuadre_2, textvariable = replace[9], width = 10).grid(row = 9, column = 1, pady = 3, padx = 5)
    senal11 = ttk.Entry(encuadre_2, textvariable = replace[10], width = 10).grid(row = 10, column = 1, pady = 3, padx = 5)
    senal12 = ttk.Entry(encuadre_2, textvariable = replace[11], width = 10).grid(row = 11, column = 1, pady = 3, padx = 5)
    senal13 = ttk.Entry(encuadre_2, textvariable = replace[12], width = 10).grid(row = 12, column = 1, pady = 3, padx = 5)
    senal14 = ttk.Entry(encuadre_2, textvariable = replace[13], width = 10).grid(row = 13, column = 1, pady = 3, padx = 5)
    senal15 = ttk.Entry(encuadre_2, textvariable = replace[14], width = 10).grid(row = 14, column = 1, pady = 3, padx = 5)
                                                         
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
    segunda_var1 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[0], state = 'readonly', width = 20).grid(row = 0, column = 0, pady = 3, padx = 5)
    segunda_var2 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[1], state = 'readonly', width = 20).grid(row = 1, column = 0, pady = 3, padx = 5)
    segunda_var3 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[2], state = 'readonly', width = 20).grid(row = 2, column = 0, pady = 3, padx = 5)
    segunda_var4 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[3], state = 'readonly', width = 20).grid(row = 3, column = 0, pady = 3, padx = 5)
    segunda_var5 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[4], state = 'readonly', width = 20).grid(row = 4, column = 0, pady = 3, padx = 5)
    segunda_var6 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[5], state = 'readonly', width = 20).grid(row = 5, column = 0, pady = 3, padx = 5)
    segunda_var7 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[6], state = 'readonly', width = 20).grid(row = 6, column = 0, pady = 3, padx = 5)
    segunda_var8 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[7], state = 'readonly', width = 20).grid(row = 7, column = 0, pady = 3, padx = 5)
    segunda_var9 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[8], state = 'readonly', width = 20).grid(row = 8, column = 0, pady = 3, padx = 5)
    segunda_var10 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[9], state = 'readonly', width = 20).grid(row = 9, column = 0, pady = 3, padx = 5)
    segunda_var11 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[10], state = 'readonly', width = 20).grid(row = 10, column = 0, pady = 3, padx = 5)
    segunda_var12 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[11], state = 'readonly', width = 20).grid(row = 11, column = 0, pady = 3, padx = 5)
    segunda_var13 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[12], state = 'readonly', width = 20).grid(row = 12, column = 0, pady = 3, padx = 5)
    segunda_var14 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[13], state = 'readonly', width = 20).grid(row = 13, column = 0, pady = 3, padx = 5)
    segunda_var15 = ttk.Combobox(encuadre_4, values = atributos_seleccionados, textvariable = combo2[14], state = 'readonly', width = 20).grid(row = 14, column = 0, pady = 3, padx = 5)
    
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
    
    #aplicar filtros
    aplicar = ttk.Button(encuadre_principal, text = 'Aplicar filtros', command = aplicar)
    aplicar.grid(row = 1, column = 1, padx = 5, pady = 5)
        
    #funcion de aplicar filtros
    def aplicar():
        print('hola mundo')
        print('aplicando filtros...')
        global df
        
        #separo vector de fechas 
        date = pd.DataFrame(df['fecha'])
        
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
        
        for variable in range(0,len(main_variables)):
            
            if str(main_variables[variable]) != '':
                variables_principales.append(main_variables[variable])
                            
            if second_variables[variable] != '':
                variables_secundarias.append(second_variables[variable])
                
            if replace_value[variable] != '':
                variables_reemplazo.append(replace_value[variable])
                
            if consecutives[variable] != '':
                variables_consecutivo.append(str(consecutives[variable]))
                
            if pendientes[variable] != '':
                variables_pendientes.append(pendientes[variable])
                
            if comparadores[variable] != '':
                variables_comparadores.append(comparadores[variable])
                
            if valores_comparadores[variable] != '':
                variables_comparacion.append(valores_comparadores[variable])
            
            if acciones[variable] != '':
                variables_accion.append(acciones[variable])
            
        # print(len(variables_consecutivo))
        #elimino variable no utilizadas
        del(main_variables, second_variables, comparadores, valores_comparadores, acciones)
        #luego de este paso me quedo con vectores que contienen unicamente las variables seleccionadas 
        
    ##############################################################################
    ################### APLICACION DE FILTROS ####################################
    ##############################################################################
            
    # FILTRO DE DATOS CONSECUTIVOS
        # para cada una de las variables seleccionadas se aplica el filtro
        # se crea un dataframe "filtrados" que donde se cumple la condición de datos consecutivos
        # se añade el índice a dicho dataframe
        # luego se aplica el where mirando la condición de si se repite el índice del dataframe principal
        # en el filtrados, en caso de que se repita se aplica la variable de reemplazo y si no el valor no cambia
        for var in range(0,len(variables_principales)):    
            
            # caso de accion "Reemplazar"
            filtrados = df.groupby((df[variables_principales[var]].shift() != df[variables_principales[var]]).\
                                  cumsum()).filter(lambda x: len(x) >= int(variables_consecutivo[var]))  
            print(filtrados)
            df[variables_principales[var]] = np.where(df.index.isin(filtrados.index), variables_reemplazo[var], df[variables_principales[var]][:])
            
            #recorrer dataframe para comparar cada valor con el valor de reemplazo
            for col in range(0,len(df.columns)):         # recorro columnas
                for fila in range(0, len(df.iloc[:,1])): # recorro filas
                    # comparar cada valor con la señal de reemplazo
                    if variables_reemplazo[var] == df.iloc[fila,col]:
                        # detallar cada caso segun la accion seleccionada 
                        # "Eliminar diezminutal"
                        if variables_accion[var] == "Eliminar diezminutal":
                            df = df.drop([fila])
                        # "Reemplazar varios"
                        elif variables_accion[var] == 'Reemplazar varios':
                            df.iloc[fila,:] = replace_value[var]
                            df['fecha'][fila] = date['fecha'][fila]
            
            
    # # FILTRO DE PENDIENTES CONSECUTIVAS
        # for col in range(1,len(df.columns)):
        #     for fila in range(0,len(df)):
        #         df.iloc[fila,col] = float(df.iloc[fila,col])
                
        # df_auxiliar = df
        # for var in range(0,len(variables_principales)):
        #     df_auxiliar = df[variables_principales[var]] - df[variables_principales[var]].shift()
        #     print("funciono...")
        #     # filtrados = df_auxiliar.groupby([df_auxiliar,df_auxiliar.diff().ne(0).cumsum()]).transform('size').ge(int(variables_pendientes[var]))
        #     print(filtrados)
        #     filtrados = df_auxiliar.groupby((df_auxiliar[variables_principales[var]].shift() != df_auxiliar[variables_principales[var]]).\
        #                                     cumsum()).filter(lambda x:len(x) >= int(variables_pendientes[var]))
        #     df[variables_principales[var]] = np.where(df.index.isin(filtrados.index), variables_reemplazo[var], df[variables_principales[var]][:])
        
        
    # FILTROS CONDICIONALES
    # estos filtros funcionan de la siguiente manera:
        #1-recorro vector de variables principales seleccionadas
        #2-analizo comparador lógico
        #3-recorro todos los valores de una columna
        #4-realizo comparacion, a la variable de comparacion la transformo en float para evitar errores de valores con coma
        #5-analizo accion a tomar luego de comparar
        #a-si la accion es "reemplazar", reemplazo el valor actual por el valor de reemplazo definido por usuario
        #b-si la accion es "reemplazar varios", reemplazo toda la fila, excepto el diezminutal, por el valor de reempazo 
            #para no reemplzar el diezminutal lo que hago es volver a copiar el valor del dzm sobre su lugar original
        #c-si la accion es "eliminar diezminutal", lo que hago es reescribir el dataframe, aplicando un drop en cada fila que no pase el filtro
    
        for var in range(0,len(variables_principales)):
            
            if variables_comparadores[var] == '>':         
                for fila in range(0,len(df['potencia'])):              
                    if df[variables_secundarias[var]][fila] > float(variables_comparacion[var]): 
                        if variables_accion[var] == 'Reemplazar':
                            df[variables_principales[var]][fila] = replace_value[var]            
                        elif variables_accion[var] == 'Reemplazar varios':
                            df.iloc[fila,:] = replace_value[var]
                            df['fecha'][fila] = date['fecha'][fila]
                        elif variables_accion[var] == 'Eliminar diezminutal':
                            df = df.drop([fila])
                          
            if variables_comparadores[var] == '<':            
                for fila in range(0,len(df['potencia'])):                
                    if df[variables_secundarias[var]][fila] < float(variables_comparacion[var]):            
                        df[variables_principales[var]][fila] = replace_value[var]                    
                    elif variables_accion[var] == 'Reemplazar varios':
                            df.iloc[fila,:] = replace_value[var]           
                            df['fecha'][fila] = date['fecha'][fila]
                    elif variables_accion[var] == 'Eliminar diezminutal':
                            df = df.drop([fila])
                        
            if variables_comparadores[var] == '=':            
                for fila in range(0,len(df['potencia'])):                
                    if df[variables_secundarias[var]][fila] == float(variables_comparacion[var]):            
                        if variables_accion[var] == 'Reemplazar':
                            df[variables_principales[var]][fila] = replace_value[var]            
                        elif variables_accion[var] == 'Reemplazar varios':
                            df.iloc[fila,:] = replace_value[var]           
                            df['fecha'][fila] = date['fecha'][fila]
                        elif variables_accion[var] == 'Eliminar diezminutal':
                            df = df.drop([fila])
                                              
            if variables_comparadores[var] == '!=':            
                for fila in range(0,len(df['potencia'])):                
                    if df[variables_secundarias[var]][fila] != float(variables_comparacion[var]):            
                        if variables_accion[var] == 'Reemplazar':
                            df[variables_principales[var]][fila] = replace_value[var]            
                        elif variables_accion[var] == 'Reemplazar varios':
                            df.iloc[fila,:] = replace_value[var]    
                            df['fecha'][fila] = date['fecha'][fila]
                        elif variables_accion[var] == 'Eliminar diezminutal':
                            df = df.drop([fila])
                                                    
            if variables_comparadores[var] == '<=':            
                for fila in range(0,len(df['potencia'])):                
                    if df[variables_secundarias[var]][fila] <= float(variables_comparacion[var]):            
                        if variables_accion[var] == 'Reemplazar':
                            df[variables_principales[var]][fila] = replace_value[var]            
                        elif variables_accion[var] == 'Reemplazar varios':
                            df.iloc[fila,:] = replace_value[var]
                            df['fecha'][fila] = date['fecha'][fila]
                        elif variables_accion[var] == 'Eliminar diezminutal':
                            df = df.drop([fila])
                                              
            if variables_comparadores[var] == '>=':            
                for fila in range(0,len(df['potencia'])):                
                    if df[variables_secundarias[var]][fila] >= float(variables_comparacion[var]):            
                        if variables_accion[var] == 'Reemplazar':
                            df[variables_principales[var]][fila] = replace_value[var]
                        elif variables_accion[var] == 'Reemplazar varios':
                            df.iloc[fila,:] = replace_value[var]           
                            df['fecha'][fila] = date['fecha'][fila]
                        elif variables_accion[var] == 'Eliminar diezminutal':
                            df = df.drop([fila])
     

#############################################################################
########################CONFIGURACION GUI####################################
#############################################################################
#DECLARACION DE VARIABLES GLOBALES

#array para guardar ruta del objeto 
ruta = []
#conexion a servidor
connect_to_PISystem('PIDataCollective')
connect_to_Server('PIDataCollective')

#se crea dataframe de pandas para contener los datos cargados
df = pd.DataFrame()
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
condiciones = ['(<) menor a ', '(>) mayor a', '(=) igual a', '(!=) diferente a', '(<=) menor o igual a', '(>=) mayor o igual a']
suplantar = ['nan', 'hueco', 'otro']

##############################################################################

#ventana principal
ventana = tkinter.Tk()
ventana.title('Consulta de datos PI')
#ventana.attributes('-fullscreen', True)
#ventana.configure(bg='black')

#logo
logo = tkinter.PhotoImage(file='logo.png')
logo_label = tkinter.Label(ventana, image = logo)
logo_label.grid(row = 0, column = 0, columnspan = 3, padx = 30, pady = 5, sticky = N + W)

#SELECCION DE ELEMENTOS Y ATRIBUTOS
#cuadro de trabajo principal
main_cuadro = tkinter.LabelFrame(ventana)
main_cuadro.grid(row = 1, column = 0, pady = 2, padx = 5, sticky = W + S + E + N)
#cuadro de texto "selecion de periodo"
cuadro = tkinter.LabelFrame(main_cuadro, text = "Parámetros de consulta")#este cuadro quedo sin titulo
cuadro.grid(row = 1, column = 0, pady = 10, padx = 5, sticky = W + E)
#etiqueta de ruta
mostrar_ruta = StringVar()
mostrar_ruta.set('')
ruta_label = tkinter.Label(cuadro, textvariable = mostrar_ruta, fg = 'red').grid(row = 5, column = 0, columnspan = 5, sticky = W + E)



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
lista_atributos = tkinter.Listbox(select_var_cuadro, width = 40, yscrollcommand=scroll_atributos.set)
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
lista_seleccionados = tkinter.Listbox(select_var_cuadro, width = 40, yscrollcommand=scroll_seleccionados.set)
lista_seleccionados.grid(row = 3 , column = 6)
scroll_seleccionados.config(command = lista_seleccionados.yview)
scroll_seleccionados.grid(row = 3, column = 7)
#BOTON ELIMINAR
delete_boton = tkinter.Button(select_var_cuadro, text = 'Quitar', command = quitar_seleccion).grid(row = 4, column = 6, pady = 3)

#texto etiqueta de estado
estado_txt = StringVar()
estado_txt.set('')
#etiqueta de estado
estado = tkinter.Label(ventana, textvariable = estado_txt, fg = 'red').grid(row = 10, column = 0, columnspan = 3, sticky = W + E)

#fechas-->etiquetas, variables,seteo inicial
fecha_ini_lbl = tkinter.Label(frame_fechas, text = 'Fecha de Inicio').grid(row = 1, column = 0, padx = 5)
fecha_ini_var = StringVar()
fecha_ini_var.set('01/01/2019 00:00')
fecha_ini_entry = tkinter.Entry(frame_fechas, textvariable = fecha_ini_var).grid(row = 2, column = 0, padx = 5, pady = 5)

fecha_fin_lbl = tkinter.Label(frame_fechas, text = 'Fecha de Fin').grid(row = 3, column = 0, padx = 5)
fecha_fin_var = StringVar()
fecha_fin_var.set('01/01/2019 00:50')
fecha_fin_entry = tkinter.Entry(frame_fechas, textvariable = fecha_fin_var).grid(row = 4, column = 0, padx = 5, pady = 5)

#etiqueta de estado
estado = tkinter.Label(ventana, textvariable = estado_txt, fg = 'red').grid(row = 10, column = 0, columnspan = 3, sticky = W + E)

#boton de carga -- crea dataframe
cargar_datos = tkinter.Button(frame_fechas, text = 'Cargar', command = cargarDatos).grid(row = 5, column = 0, pady = 5, padx = 5, sticky = W + E)

#etiqueta de estado
estado = tkinter.Label(ventana, textvariable = estado_txt, fg = 'red').grid(row = 10, column = 0, columnspan = 3, sticky = W + E)

#boton de exportar datos -- crea csv    
exporta_datos = tkinter.Button(frame_fechas, text = 'Exportar', state = DISABLED, command = exportarDatos)
exporta_datos.grid(row = 6, column = 0, pady = 5, padx = 5, sticky = W + E)

##############################################################################
####################REPLICAR DATOS PARA OTROS AGs#############################
##############################################################################

#cuadro de adorno
cuadro_sin_name = tkinter.LabelFrame(main_cuadro)
cuadro_sin_name.grid(row = 2, column = 0, sticky = W, pady = 5, padx = 5)
#cuadro aerogeneradores principal
ags_var_cuadro = tkinter.LabelFrame(cuadro_sin_name, text = "Replicar variables para otros Ags")
ags_var_cuadro.grid(row = 1, column = 1, padx = 5, sticky = N + E, pady = 5)

#cuadro de seleccion de aerogeneradores
ags_sel_cuadro = tkinter.LabelFrame(ags_var_cuadro, text = "Seleccion de aerogeneradores")
ags_sel_cuadro.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = W + E + N + S)

#VARIABLES SELECCIONADAS
var_selected_lbl = tkinter.Label(ags_sel_cuadro, text = "Variables seleccionadas").grid(row = 0, column = 1, pady = 1, padx = 5)
#lista de variables seleccionadas
scroll_var_selected = tkinter.Scrollbar(ags_sel_cuadro, orient = VERTICAL)
refresh_button = tkinter.Button(ags_sel_cuadro, text = "Importar variables", state = DISABLED, command = lista_variables)
refresh_button.grid(row = 2, column = 1, pady = 5, sticky = W + E)
lista_var_selected = tkinter.Listbox(ags_sel_cuadro, width = 25, height = 10, yscrollcommand=scroll_var_selected.set)
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
btn_load_ags = tkinter.Button(ags_sel_cuadro, text = "Lista AGs", command = lista_ags).grid(row = 2, column = 4, pady = 5, padx = 5, sticky = W + E)  
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
btn_add_ag = tkinter.Button(ags_sel_cuadro, text = "Agregar", command = agregar_ag).grid(row = 2, column = 7, padx = 2, sticky = W)
btn_quit_ag = tkinter.Button(ags_sel_cuadro, text = "Quitar", command = quitar_ag).grid(row = 2, column = 7, padx = 2, sticky = E)
btn_add_all = tkinter.Button(ags_sel_cuadro, text = "Agregar todos", command = agregar_todos).grid(row = 3, column = 7, pady = 2, sticky = W + E)
#btn_quit_all = tkinter.Button(ags_sel_cuadro, text = "Quitar todos").grid(row = 3, column = 7, pady = 2, sticky = E)

#se crea boton temporal para funcion de generar atributos en todos los ags
# btn_crear_atributos = tkinter.Button(ags_var_cuadro, text = "Crear atributos para AGs seleccionados", command = crear_atributos_varios_ags)
# btn_crear_atributos.grid(row = 0, column = 2, padx = 5, pady = 5, columnspan = 4)

#cuadro de exportacion y creacion de variables para varios ags
acciones = tkinter.LabelFrame(ags_var_cuadro, text = "AGs seleccionados")
acciones.grid(row = 0, column = 1, sticky = N + S, padx = 5, pady = 5)
#se crea boton temporal para funcion de generar atributos en todos los ags
btn_crear_atributos = tkinter.Button(acciones, text = "Replicar variables", state = DISABLED, command = crear_atributos_varios_ags)
btn_crear_atributos.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W + E)
#botones cargar y exportar datos de todos los aerogeneradores
cargar_datos_aeros = tkinter.Button(acciones, text = "Exportar", state = DISABLED, command = cargar_datos_ags)
cargar_datos_aeros.grid(row = 1, column = 0, pady = 5, padx = 5, sticky = W + E)
#export_datos_aeros = tkinter.Button(ags_var_cuadro, text = "Exportar datos").grid(row = 1, column = 4, pady = 5, sticky = E)

##############################################################################
####################### VENTANA DE FILTROS ###################################
##############################################################################
#cuadro de orden
encuadre_1 = tkinter.LabelFrame(main_cuadro)
encuadre_1.grid(row = 2, column = 0, pady = 5, padx = 5, sticky = E + S + N)
#cuadro principal
marco_validacion =  tkinter.LabelFrame(encuadre_1, text = 'Validacion de Datos')
marco_validacion.grid(row = 0, column = 0, pady = 5, padx = 5)

#ir a ventana de filtros
filtros_btn = tkinter.Button(marco_validacion, text = 'Validacion y Filtros', state = DISABLED, command = ventana_filtros)
filtros_btn.grid(row = 0, column = 0, pady = 5, padx = 5)


#funcion de actualizacion de listas, muy muy importante para que esto ande
actualizar_listado(listado_actual, lista_elementos)
ventana.mainloop()
#valentineseolico2018