# piQuery
GUI para consulta a base de datos corporativa

piQuery es una interfaz gráfica creada para interactuar con una base de datos que gestiona información de parques eólicos.
La idea principal de la aplicación es poder traer información desde la base de datos, de una o muchas variables, en un entorno de tiempo seleccionado por el usuario.
Cuenta con funciones para facilitar la consulta, como por ejemplo escoger una única variable de un aerogenerador y poder replicarla para los aerogeneradores que el usuario necesite.
También cuenta con set de datos predefinidos, que cargan una lista de variables ya definida, lo que facilita la elección de las variables a trabajar.
Se cuenta con una pestaña utilizada para filtrar los datos seleccionados, donde se pueden aplicar filtros condicionales, filtros de datos truncados, filtros cruzados entre variables y filtros de datos ausentes.
La información extraída y filtrada se puede exportar en forma de archivo .csv para luego ser utilizada por el usuario de la manera que más le sirva.

El programa está escrito completamente en python.
Utiliza la librería Tkinter para el manejo de la interfaz gráfica, para el manejo y procesamiento de datos se utiliza Pandas y Numpy.
Se hace manejos de series temporales, se utilizan librerías que interactúan directamente con el sistema operativo.
El programa finalmente se lo transforma a .exe, para que pueda ser ejecutado por cualquier usuario.
