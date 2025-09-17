# %%
# %%
import requests
#import mysql.connector
import os
from dotenv import load_dotenv
#import json
import pandas as pd
import pymysql
import time
from datetime import datetime, timedelta

load_dotenv()

# %%
# Configuración API
API_BASE_URL = "https://cramer.buk.cl/api/v1/chile/"
API_ENDPOINTS = {
    "licences": f"{API_BASE_URL}absences/licence",
    "absences": f"{API_BASE_URL}absences/absence",
    "permissions": f"{API_BASE_URL}absences/permission"
}
TOKEN = os.getenv("BUK_AUTH_TOKEN")

# Configuración BD
DB_HOST = os.getenv("IP") #REEMPLAZAR HOST SI ES DISTINTO
DB_USER = "rrhh_master" #REEMPLAZAR USUARIO CREADO POR GABRIEL Y CONTRASEÑA
DB_PASSWORD = os.getenv("clave_sql") #REEMPLAZAR CONTRASEÑA CREADA POR GABRIEL
DB_NAME = "rrhh_app" #REEMPLAZAR NOMBRE DE BASE DE DATOS CREADA POR GABRIEL

# Imprimir las variables de entorno
print(f"TOKEN: {os.getenv('BUK_AUTH_TOKEN')}")
print(f"SQL: {os.getenv('clave_sql')}")
print(f"IP: {os.getenv('IP')}")

# %%
# --- Configuración de Filtro por Rango de Fechas ---

fecha_hoy = datetime.now().date()
fecha_inicio_objetivo = fecha_hoy - timedelta(days=7)

# Cambia a True para activar el filtro por fechas. Si es False, extraerá todos los datos.
FILTRAR_POR_FECHAS = True

# Define el rango de fechas si FILTRAR_POR_FECHAS es True. Formato: "YYYY-MM-DD"
# La API de BUK filtra por la fecha de inicio de la incidencia.
FECHA_INICIO = fecha_inicio_objetivo.strftime("%Y-%m-%d")
FECHA_FIN = fecha_hoy.strftime("%Y-%m-%d")

if FILTRAR_POR_FECHAS:
    print(f"🗓️ FILTRO POR FECHAS ACTIVADO: Se extraerán datos entre {FECHA_INICIO} y {FECHA_FIN}.")
else:
    print("⚙️ Extrayendo todos los datos disponibles (sin filtro de fechas).")

# %%
#Mostrar los datos del primer json de cada endpoint
def mostrar_datos_endpoint(endpoint_url: str):
    """
    Returns:
        list: Una lista con todos los datos obtenidos.
    """
    headers = {"auth_token": TOKEN}
    todos_los_datos = []
    url_actual = endpoint_url
    pagina_actual = 1

    print(f"\n🚀 Comenzando la obtención de datos desde: {endpoint_url}")

    while url_actual and pagina_actual <= 1:
        print(f"📄 Obteniendo página {pagina_actual}...")

        try:
            respuesta = requests.get(url_actual, headers=headers, timeout=10)
            respuesta.raise_for_status()

            respuesta_api = respuesta.json()
            datos_pagina = respuesta_api.get('data', [])
            pagination_info = respuesta_api.get('pagination', {})

            todos_los_datos.extend(datos_pagina)

            print(f"✅ Página {pagina_actual}: {len(datos_pagina)} datos obtenidos")
            print(f"📊 Total acumulado: {len(todos_los_datos)} datos")
            
            total_pages = pagination_info.get('total_pages', 1)
            print(f"📈 Páginas restantes: {total_pages - pagina_actual}")

            url_actual = pagination_info.get('next')
            pagina_actual += 1

            time.sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la petición para la página {pagina_actual}: {e}")
            break

    print(f"🎉 ¡Paginación completada! Total de datos obtenidos: {len(todos_los_datos)}")
    return todos_los_datos

# Itera sobre todos los endpoints y almacena los datos en un diccionario
todos_los_datos_extraidos = {}

for nombre_endpoint, url_endpoint in API_ENDPOINTS.items():
    datos_obtenidos = mostrar_datos_endpoint(url_endpoint)
    todos_los_datos_extraidos[nombre_endpoint] = datos_obtenidos
    print(f"--- Extracción de '{nombre_endpoint}' terminada. ---")
    print(f"Primer dato de '{nombre_endpoint}': {datos_obtenidos[0] if datos_obtenidos else 'No data'}")

# %%
def construir_url_con_fechas(base_url: str, fecha_inicio: str = None, fecha_fin: str = None):
    """
    Construye la URL del endpoint con parámetros de fecha si están definidos.
    
    Args:
        base_url (str): URL base del endpoint
        fecha_inicio (str): Fecha de inicio en formato YYYY-MM-DD
        fecha_fin (str): Fecha de fin en formato YYYY-MM-DD
        
    Returns:
        str: URL completa con parámetros de fecha si aplica
    """
    if fecha_inicio and fecha_fin:
        # Agregar parámetros de fecha a la URL
        separador = "&" if "?" in base_url else "?"
        url_con_fechas = f"{base_url}{separador}from={fecha_inicio}&to={fecha_fin}"
        return url_con_fechas
    else:
        return base_url


# %%
def obtener_datos_paginados(endpoint_url: str, aplicar_filtro_fechas: bool = False, fecha_inicio: str = None, fecha_fin: str = None):
    """
    Obtiene datos paginados desde un endpoint, con opción de filtrar por fechas.
    
    Args:
        endpoint_url (str): URL del endpoint
        aplicar_filtro_fechas (bool): Si aplicar filtro de fechas
        fecha_inicio (str): Fecha de inicio en formato YYYY-MM-DD
        fecha_fin (str): Fecha de fin en formato YYYY-MM-DD
        
    Returns:
        list: Una lista con todos los datos obtenidos.
    """
    headers = {"auth_token": TOKEN}
    todos_los_datos = []
    
    # Construir la URL con filtros de fecha si es necesario
    if aplicar_filtro_fechas and fecha_inicio and fecha_fin:
        url_actual = construir_url_con_fechas(endpoint_url, fecha_inicio, fecha_fin)
        print(f"\n🚀 Comenzando extracción con filtro de fechas desde: {url_actual}")
    else:
        url_actual = endpoint_url
        print(f"\n🚀 Comenzando extracción de todos los datos desde: {endpoint_url}")
    
    pagina_actual = 1

    while url_actual:
        print(f"📄 Obteniendo página {pagina_actual}...")

        try:
            respuesta = requests.get(url_actual, headers=headers, timeout=10)
            respuesta.raise_for_status()

            respuesta_api = respuesta.json()
            datos_pagina = respuesta_api.get('data', [])
            pagination_info = respuesta_api.get('pagination', {})

            todos_los_datos.extend(datos_pagina)

            print(f"✅ Página {pagina_actual}: {len(datos_pagina)} datos obtenidos")
            print(f"📊 Total acumulado: {len(todos_los_datos)} datos")
            
            total_pages = pagination_info.get('total_pages', 1)
            print(f"📈 Páginas restantes: {total_pages - pagina_actual}")

            url_actual = pagination_info.get('next')
            pagina_actual += 1

            time.sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la petición para la página {pagina_actual}: {e}")
            break

    if aplicar_filtro_fechas:
        print(f"🎉 ¡Extracción con filtro de fechas completada! Total: {len(todos_los_datos)} datos")
    else:
        print(f"🎉 ¡Extracción completa terminada! Total: {len(todos_los_datos)} datos")
        
    return todos_los_datos

# Ejemplo de uso con el segmentador de fechas
todos_los_datos_extraidos = {}

for nombre_endpoint, url_endpoint in API_ENDPOINTS.items():
    print(f"\n🔄 --- Procesando endpoint: '{nombre_endpoint}' ---")
    
    if FILTRAR_POR_FECHAS:
        datos_obtenidos = obtener_datos_paginados(
            url_endpoint, 
            aplicar_filtro_fechas=True, 
            fecha_inicio=FECHA_INICIO, 
            fecha_fin=FECHA_FIN
        )
    else:
        datos_obtenidos = obtener_datos_paginados(url_endpoint)
    
    todos_los_datos_extraidos[nombre_endpoint] = datos_obtenidos
    print(f"--- Extracción de '{nombre_endpoint}' terminada. {len(datos_obtenidos)} registros obtenidos ---")

# %%
try:
    print("🚀 Conectando a MySQL...")
    conexion = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )
    cursor = conexion.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    print(f"✅ Conectado a MySQL y usando la base: {DB_NAME}")
except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")
    exit()

def crear_e_insertar_tabla_actualiza(nombre_tabla: str, datos: list):
    """
    Crea una tabla en la base de datos y la llena solo con registros nuevos o actualiza los existentes.
    """
    if not datos:
        print(f"⚠️ No hay datos para la tabla '{nombre_tabla}'. Saliendo...")
        return

    columnas = list(datos[0].keys())
    columnas_con_tipos = [f"{col} VARCHAR(255)" for col in columnas]

    # Asegurarse de que el 'id' sea la clave primaria
    if 'id' in columnas_con_tipos:
        id_index = columnas_con_tipos.index('id VARCHAR(255)')
        columnas_con_tipos[id_index] = 'id INT PRIMARY KEY'

    column_definitions = ", ".join(columnas_con_tipos)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({column_definitions})"
    cursor.execute(create_table_sql)

    print(f"🚀 Insertando o actualizando registros en la tabla '{nombre_tabla}'...")

    # Construir la parte de actualización para ON DUPLICATE KEY UPDATE
    update_clause = ", ".join([f"{col}=VALUES({col})" for col in columnas if col != 'id'])

    sql_insert = f"""
    INSERT INTO {nombre_tabla} ({', '.join(columnas)})
    VALUES ({', '.join(['%s'] * len(columnas))})
    ON DUPLICATE KEY UPDATE {update_clause}
    """

    contador = 0
    for item in datos:
        try:
            values = tuple(item.get(col) for col in columnas)
            cursor.execute(sql_insert, values)
            contador += cursor.rowcount  # Cuenta inserciones y actualizaciones
        except Exception as error:
            print(f"⚠️ Error insertando/actualizando registro con id {item.get('id', 'N/A')}: {error}")

    conexion.commit()
    print(f"✅ {contador} registros insertados o actualizados en '{nombre_tabla}'.")

# 1. Extraer los datos de todos los endpoints
todos_los_datos_extraidos = {}
for nombre_endpoint, url_endpoint in API_ENDPOINTS.items():
    datos_obtenidos = obtener_datos_paginados(url_endpoint, aplicar_filtro_fechas=FILTRAR_POR_FECHAS, fecha_inicio=FECHA_INICIO, fecha_fin=FECHA_FIN)
    todos_los_datos_extraidos[nombre_endpoint] = datos_obtenidos
    print(f"--- Extracción de '{nombre_endpoint}' terminada. ---")

# 2. Iterar sobre los datos extraídos e insertarlos en la BD
print("\n--- Procesando e insertando/actualizando datos en MySQL ---")
for nombre_tabla, datos in todos_los_datos_extraidos.items():
    crear_e_insertar_tabla_actualiza(nombre_tabla, datos)

# 3. Mostrar estadísticas por tabla
print("\n--- Consultando estadísticas de las tablas ---")
for nombre_tabla in todos_los_datos_extraidos.keys():
    try:
        cursor.execute(f"SELECT COUNT(*) as total FROM {nombre_tabla};")
        total_registros = cursor.fetchone()[0]
        print(f"📊 Total de registros en la tabla '{nombre_tabla}': {total_registros}")

        print(f"🔍 Mostrando los primeros 3 registros de '{nombre_tabla}':")
        cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 3;")
        column_names = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            print(dict(zip(column_names, row)))

    except Exception as e:
        print(f"❌ Error al consultar la tabla '{nombre_tabla}': {e}")


with open(r"C:\Users\bgacitua\Desktop\Repositorio_Compartido_GitHub\logs_rflex", 'a') as f:
        f.write(f"{datetime.now()}: Sincronización completada\n")

# --- Cierre de conexión ---
cursor.close()
conexion.close()
print("\n✅ Conexión cerrada correctamente.")


