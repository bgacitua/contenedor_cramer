import requests
import pymysql
import time
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_datos_paginados(endpoint_url: str, token: str):
    """
    Obtiene todos los datos paginados de un endpoint de la API.
    
    Args:
        endpoint_url (str): URL del endpoint de la API
        token (str): Token de autenticación
        
    Returns:
        list: Una lista con todos los datos obtenidos.
    """
    headers = {"auth_token": token}
    todos_los_datos = []
    url_actual = endpoint_url
    pagina_actual = 1

    print(f"\n🚀 Comenzando la obtención de datos desde: {endpoint_url}")

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

    print(f"🎉 ¡Paginación completada! Total de datos obtenidos: {len(todos_los_datos)}")
    return todos_los_datos


def crear_e_insertar_tabla_actualiza(cursor, conexion, nombre_tabla: str, datos: list):
    """
    Crea una tabla en la base de datos y la llena solo con registros nuevos o actualiza los existentes.
    
    Args:
        cursor: Cursor de la conexión a MySQL
        conexion: Conexión a MySQL
        nombre_tabla (str): Nombre de la tabla a crear/actualizar
        datos (list): Lista de diccionarios con los datos
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


def conectar_mysql(db_host, db_user, db_password, db_name):
    """
    Conecta a MySQL y retorna la conexión y cursor.
    
    Args:
        db_host (str): Host de la base de datos
        db_user (str): Usuario de la base de datos
        db_password (str): Contraseña de la base de datos
        db_name (str): Nombre de la base de datos
        
    Returns:
        tuple: (conexion, cursor)
    """
    try:
        print("🚀 Conectando a MySQL...")
        conexion = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            charset='utf8mb4'
        )
        cursor = conexion.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Crear tabla de log si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_cargas_api (
                endpoint VARCHAR(100),
                ultima_fecha DATETIME,
                ultimo_id INT,
                PRIMARY KEY (endpoint)
            )
        """)
        conexion.commit()
        
        print(f"✅ Conectado a MySQL y usando la base: {db_name}")
        return conexion, cursor
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        raise e


def obtener_ultima_carga(cursor, endpoint):
    """
    Obtiene la información de la última carga para un endpoint específico.
    
    Args:
        cursor: Cursor de la conexión a MySQL
        endpoint (str): Nombre del endpoint
        
    Returns:
        dict: Información de la última carga
    """
    cursor.execute("SELECT ultima_fecha, ultimo_id FROM log_cargas_api WHERE endpoint = %s", (endpoint,))
    result = cursor.fetchone()
    
    if result:
        return {
            'ultima_fecha': result[0],
            'ultimo_id': result[1]
        }
    return None


def actualizar_log_carga(cursor, conexion, endpoint, datos):
    """
    Actualiza el log de cargas con la información más reciente.
    
    Args:
        cursor: Cursor de la conexión a MySQL
        conexion: Conexión a MySQL
        endpoint (str): Nombre del endpoint
        datos (list): Lista de datos cargados
    """
    if not datos:
        return
    
    # Obtener la fecha y ID más recientes de los datos
    ultima_fecha = None
    ultimo_id = 0
    
    for item in datos:
        if 'created_at' in item and item['created_at']:
            if ultima_fecha is None or item['created_at'] > ultima_fecha:
                ultima_fecha = item['created_at']
        
        if 'id' in item and item['id']:
            if int(item['id']) > ultimo_id:
                ultimo_id = int(item['id'])
    
    # Actualizar el log
    cursor.execute("""
        INSERT INTO log_cargas_api (endpoint, ultima_fecha, ultimo_id)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            ultima_fecha = VALUES(ultima_fecha),
            ultimo_id = VALUES(ultimo_id)
    """, (endpoint, ultima_fecha, ultimo_id))
    conexion.commit()
    
    print(f"📝 Log actualizado para '{endpoint}': última fecha={ultima_fecha}, último ID={ultimo_id}")


def construir_url_incremental(base_url, endpoint, ultima_carga):
    """
    Construye una URL con filtros para obtener solo datos nuevos.
    
    Args:
        base_url (str): URL base de la API
        endpoint (str): Nombre del endpoint
        ultima_carga (dict): Información de la última carga
        
    Returns:
        str: URL con filtros aplicados
    """
    url = f"{base_url}employees/absences/{endpoint}"
    
    if ultima_carga and ultima_carga['ultimo_id']:
        # Filtrar por ID mayor al último cargado
        url += f"?id_gt={ultima_carga['ultimo_id']}"
        print(f"🔍 Consultando {endpoint} con ID > {ultima_carga['ultimo_id']}")
    else:
        print(f"🔍 Primera carga de {endpoint} - obteniendo todos los datos")
    
    return url

