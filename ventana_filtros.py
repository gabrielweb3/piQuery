from tkinter import *
from tkinter import ttk
import tkinter

import pandas as pd
import numpy as np

def aplicar():
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
                                                                                
def callback_function():
    print(combo[0].get())
    
    
##############################################################################
######################### VARIABLES GLOBALES #################################
##############################################################################
#textdata.csv
atributos_seleccionados = []
df = pd.read_csv('textdata.csv')

#variable de variables para menu desplegable
for columna in range(1,len(df.columns)):
    atributos_seleccionados.append(df.columns[columna])
    
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
var1 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[0], state = 'readonly', width = 20).grid(row = 0, column = 0, pady = 3, padx = 5)
var2 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[1], state = 'readonly', width = 20).grid(row = 1, column = 0, pady = 3, padx = 5)
var3 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[2], state = 'readonly', width = 20).grid(row = 2, column = 0, pady = 3, padx = 5)
var4 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[3], state = 'readonly', width = 20).grid(row = 3, column = 0, pady = 3, padx = 5)
var5 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[4], state = 'readonly', width = 20).grid(row = 4, column = 0, pady = 3, padx = 5)
var6 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[5], state = 'readonly', width = 20).grid(row = 5, column = 0, pady = 3, padx = 5)
var7 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[6], state = 'readonly', width = 20).grid(row = 6, column = 0, pady = 3, padx = 5)
var8 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[7], state = 'readonly', width = 20).grid(row = 7, column = 0, pady = 3, padx = 5)
var9 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[8], state = 'readonly', width = 20).grid(row = 8, column = 0, pady = 3, padx = 5)
var10 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[9], state = 'readonly', width = 20).grid(row = 9, column = 0, pady = 3, padx = 5)
var11 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[10], state = 'readonly', width = 20).grid(row = 10, column = 0, pady = 3, padx = 5)
var12 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[11], state = 'readonly', width = 20).grid(row = 11, column = 0, pady = 3, padx = 5)
var13 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[12], state = 'readonly', width = 20).grid(row = 12, column = 0, pady = 3, padx = 5)
var14 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[13], state = 'readonly', width = 20).grid(row = 13, column = 0, pady = 3, padx = 5)
var15 = ttk.Combobox(encuadre_1, values = atributos_seleccionados, textvariable = combo[14], state = 'readonly', width = 20).grid(row = 14, column = 0, pady = 3, padx = 5)
 
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


ventana_filtros.mainloop()

#https://stackoverflow.com/questions/50607811/how-to-display-combobox-in-tkinter
