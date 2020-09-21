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
        
    
## VENTANA DE FILTROS ##

    
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
filtros_btn = tkinter.Button(marco_validacion, text = 'Validacion y Filtros',
                             
                             state = DISABLED)
filtros_btn.grid(row = 0, column = 0, pady = 5, padx = 5)


#funcion de actualizacion de listas, muy muy importante para que esto ande
actualizar_listado(listado_actual, lista_elementos)
ventana.mainloop()
#valentineseolico2018