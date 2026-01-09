### \# Zona FIT GYM

Este pequeño proyecto se trata de una aplicación hecha en python, con una interfaz gráfica hecha en tkinter.

Donde mediante esta interfaz se puede interactuar con una base de datos de un gimnasio, para guardar clientes del mismo.



#### \# Instrucciones para inicializar el proyecto



##### Tener instalado:

\- python 3.9 o superior

\- MySQL instalado (Opcional es tener MySQL Workbench)

\- Liberias de Python indicadas en requirements.txt



##### NO es necesario:

\- Crear una base de datos desde cero, en la carpeta <<db>> se incluyen los archivos schema.sql y data.sql para importar todo de una vez



##### Configura las variables de entorno para el proyecto (.env)

Este proyecto requiere de ciertas variables de entorno, principalmente para que la conexión con la base de datos funcione correctamente, a continuación el archivo .env debe estar en la raíz de la carpeta del proyecto y debe de contener los siguientes valores de esta forma:

DB\_NAME = "El nombre de la base de datos"

DB\_HOST = "localhost"

DB\_PASS = "password"

DB\_USER = "user"



##### Por último podes ejecutar este comando sql para crear la base de datos con tablas y datos de prueba listos:

CREATE DATABASE clientes\_db;

USE clientes\_db;

SOURCE db/schema.sql;

SOURCE db/data.sql;



