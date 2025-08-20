#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE RESPALDO AUTOMATIZADO - BIOMÉTRICO MORPHO
====================================================

Este script automatiza la "fotografía diaria" del sistema biométrico,
generando respaldos CSV con datos de asistencia sin intervención manual.

Funcionalidades:
- Conexión automática a SQL Server MorphoManager
- Consulta datos de asistencia del mes actual
- Genera archivo CSV con timestamp único
- Sistema de logging para monitoreo
- Rotación automática de archivos antiguos
- Manejo de errores robusto

Programación recomendada: Diario a las 23:30 hrs
"""

import pyodbc
import pandas as pd
import datetime
import os
import logging
import sys
from pathlib import Path

class RespaldoBiometrico:
    def __init__(self):
        """Inicializa el sistema de respaldo biométrico"""
        
        # Configuración de base de datos
        self.SERVER = '192.9.200.84'
        self.DATABASE = 'MorphoManager'
        self.USERNAME = 'rrhh_morpho'
        self.PASSWORD = 'PQ90@ZT*'
        
        # Configuración de archivos
        self.BASE_DIR = Path(r"C:\Users\bgacitua\Desktop\Repositorio_GitHub\Scripts de Python")
        self.RESPALDOS_DIR = self.BASE_DIR / "Respaldos_Biometrico"
        self.LOGS_DIR = self.BASE_DIR / "Logs"
        
        # Crear directorios si no existen
        self.RESPALDOS_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
        
        # Configurar logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configura el sistema de logging"""
        log_filename = self.LOGS_DIR / f"respaldo_biometrico_{datetime.date.today().strftime('%Y%m')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def conectar_bd(self):
        """Establece conexión con SQL Server MorphoManager"""
        try:
            connection_string = (
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.SERVER};'
                f'DATABASE={self.DATABASE};'
                f'UID={self.USERNAME};'
                f'PWD={self.PASSWORD};'
                'TrustServerCertificate=yes;'
            )
            
            cnxn = pyodbc.connect(connection_string)
            self.logger.info("✅ Conexión a SQL Server establecida exitosamente")
            return cnxn
            
        except pyodbc.Error as ex:
            self.logger.error(f"❌ Error al conectar a SQL Server: {ex}")
            if ex.args[0] == '28000':
                self.logger.error("Causa: Error de autenticación")
            elif ex.args[0] == '08001':
                self.logger.error("Causa: Servidor no accesible o puerto bloqueado")
            return None
            
    def generar_consulta_sql(self):
        """Genera la consulta SQL con fechas automáticas"""
        fecha_actual = datetime.datetime.now()
        fecha_inicio = fecha_actual.replace(day=1).strftime('%Y-%m-%d')
        fecha_fin = fecha_actual.strftime('%Y-%m-%d')
        
        self.logger.info(f"📅 Rango de consulta: {fecha_inicio} a {fecha_fin}")
        
        sql_query = f"""
        -- Respaldo automatizado biométrico - Mes actual
        DECLARE @fecha_inicio DATE = '{fecha_inicio}';
        DECLARE @fecha_fin DATE = '{fecha_fin}';

        WITH fechas_rango AS (
            SELECT @fecha_inicio AS [FECHA_SANTIAGO]
            UNION ALL
            SELECT DATEADD(DAY, 1, [FECHA_SANTIAGO])
            FROM fechas_rango
            WHERE DATEADD(DAY, 1, [FECHA_SANTIAGO]) <= @fecha_fin
        ),
        todos_trabajadores AS (
            SELECT DISTINCT 
                u.[ID] AS [USER_ID],
                u.[FIRSTNAME],
                u.[LASTNAME],
                u.[EMPLOYEEID]
            FROM [MorphoManager].[dbo].[User_] AS u
            WHERE u.[EMPLOYEEID] IS NOT NULL 
            AND u.[EMPLOYEEID] != ''
        ),
        combinaciones_trabajador_fecha AS (
            SELECT 
                t.[USER_ID],
                t.[FIRSTNAME],
                t.[LASTNAME], 
                t.[EMPLOYEEID],
                f.[FECHA_SANTIAGO]
            FROM todos_trabajadores t
            CROSS JOIN fechas_rango f
        )
        SELECT 
            -- Información del trabajador
            ctf.[FIRSTNAME],
            ctf.[LASTNAME],
            ctf.[EMPLOYEEID],
            ctf.[FECHA_SANTIAGO],
            
            -- Conteo de registros por tipo
            COALESCE(SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'IN' THEN 1 ELSE 0 END), 0) AS [KEY_IN],
            COALESCE(SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'OUT' THEN 1 ELSE 0 END), 0) AS [KEY_OUT],
            COALESCE(SUM(CASE WHEN m.[FUNCTIONKEYTEXT] = 'No Key' THEN 1 ELSE 0 END), 0) AS [NO_KEY],
            
            -- Estado de asistencia
            CASE 
                WHEN COUNT(m.[ID]) = 0 THEN 'Ausente'
                WHEN COUNT(m.[ID]) >= 1 THEN 'Asiste'
            END AS [ESTADO_ASISTENCIA],
            
            -- Información adicional
            COALESCE(COUNT(DISTINCT bd.[NAME_]), 0) AS [CANTIDAD_DISPOSITIVOS],
            COALESCE(COUNT(m.[ID]), 0) AS [TOTAL_REGISTROS],
            
            -- Horarios
            COALESCE(MIN(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS TIME)), '00:00:00') AS [PRIMERA_MARCA],
            COALESCE(MAX(CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS TIME)), '00:00:00') AS [ULTIMA_MARCA]
            
        FROM combinaciones_trabajador_fecha ctf
        LEFT JOIN [MorphoManager].[dbo].[AccessLog] AS m 
            ON ctf.[USER_ID] = m.[USERID]
            AND ctf.[FECHA_SANTIAGO] = CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE)
            AND CAST(m.[LOGDATETIME] AT TIME ZONE 'UTC' AT TIME ZONE 'Pacific SA Standard Time' AS DATE) BETWEEN @fecha_inicio AND @fecha_fin
        LEFT JOIN [MorphoManager].[dbo].[BiometricDevice] AS bd 
            ON m.[MORPHOACCESSID] = bd.[ID]
            
        GROUP BY 
            ctf.[FIRSTNAME],
            ctf.[LASTNAME],
            ctf.[EMPLOYEEID],
            ctf.[FECHA_SANTIAGO],
            ctf.[USER_ID]
            
        ORDER BY 
            ctf.[LASTNAME], ctf.[FIRSTNAME], ctf.[FECHA_SANTIAGO] DESC
        OPTION (MAXRECURSION 366);
        """
        
        return sql_query
    
    def procesar_dataframe(self, df):
        """Procesa y limpia el DataFrame"""
        self.logger.info("🔧 Procesando DataFrame...")
        
        # Separar DV del RUT
        tiene_delimitador = df['EMPLOYEEID'].astype(str).str.contains('-')
        df['ID_ADICIONAL'] = df['EMPLOYEEID'].astype(str).str.split('-').str[1].fillna('')
        df.loc[tiene_delimitador, 'EMPLOYEEID'] = df.loc[tiene_delimitador, 'EMPLOYEEID'].astype(str).str.split('-').str[0]
        
        # Convertir EMPLOYEEID a numérico
        df['EMPLOYEEID'] = pd.to_numeric(df['EMPLOYEEID'], errors='coerce')
        
        # Crear columnas de búsqueda
        df['EMPLOYEEID_STR'] = df['EMPLOYEEID'].astype(str).str.replace(r'\.0$', '', regex=True)
        df['FECHA_SANTIAGO_STR'] = df['FECHA_SANTIAGO'].astype(str)
        df['BusquedaRUT'] = df['EMPLOYEEID_STR'] + ";" + df['FECHA_SANTIAGO_STR']
        
        # Agregar metadatos del respaldo
        df['TIMESTAMP_RESPALDO'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['TIPO_RESPALDO'] = 'AUTOMATICO'
        
        self.logger.info(f"✅ DataFrame procesado: {len(df):,} registros, {len(df.columns)} columnas")
        return df
    
    def exportar_csv(self, df):
        """Exporta el DataFrame a archivo CSV"""
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = self.RESPALDOS_DIR / f"Respaldo_Morpho_AccessLog_{timestamp_str}.csv"
        
        try:
            # Exportar con configuraciones optimizadas
            df.to_csv(nombre_archivo, 
                     index=False, 
                     encoding='utf-8-sig', 
                     sep=';',
                     date_format='%Y-%m-%d')
            
            # Obtener estadísticas del archivo
            size_kb = nombre_archivo.stat().st_size / 1024
            
            self.logger.info(f"✅ RESPALDO CSV GENERADO EXITOSAMENTE")
            self.logger.info(f"📁 Archivo: {nombre_archivo}")
            self.logger.info(f"📊 Registros: {len(df):,}")
            self.logger.info(f"📋 Columnas: {len(df.columns)}")
            self.logger.info(f"💾 Tamaño: {size_kb:.2f} KB")
            
            # Estadísticas de contenido
            self.logger.info(f"👥 Empleados únicos: {df['EMPLOYEEID'].nunique():,}")
            self.logger.info(f"📅 Fechas: {df['FECHA_SANTIAGO'].min()} a {df['FECHA_SANTIAGO'].max()}")
            self.logger.info(f"✅ Con asistencia: {(df['ESTADO_ASISTENCIA'] == 'Asiste').sum():,}")
            self.logger.info(f"❌ Ausentes: {(df['ESTADO_ASISTENCIA'] == 'Ausente').sum():,}")
            
            return nombre_archivo
            
        except Exception as e:
            self.logger.error(f"❌ Error al exportar CSV: {str(e)}")
            return None
    
    def limpiar_archivos_antiguos(self, dias_antiguedad=30):
        """Elimina archivos de respaldo antiguos"""
        try:
            fecha_limite = datetime.datetime.now() - datetime.timedelta(days=dias_antiguedad)
            archivos_eliminados = 0
            
            for archivo in self.RESPALDOS_DIR.glob("Respaldo_Morpho_AccessLog_*.csv"):
                if archivo.stat().st_mtime < fecha_limite.timestamp():
                    archivo.unlink()
                    archivos_eliminados += 1
                    
            if archivos_eliminados > 0:
                self.logger.info(f"🗑️ Eliminados {archivos_eliminados} archivos antiguos (>{dias_antiguedad} días)")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error al limpiar archivos antiguos: {str(e)}")
    
    def ejecutar_respaldo(self):
        """Ejecuta el proceso completo de respaldo"""
        inicio = datetime.datetime.now()
        self.logger.info("=" * 60)
        self.logger.info(f"🚀 INICIANDO RESPALDO AUTOMATIZADO BIOMÉTRICO")
        self.logger.info(f"🕐 Hora de inicio: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 60)
        
        try:
            # 1. Conectar a base de datos
            cnxn = self.conectar_bd()
            if not cnxn:
                raise Exception("No se pudo establecer conexión con la base de datos")
            
            # 2. Ejecutar consulta
            self.logger.info("📋 Ejecutando consulta SQL...")
            sql_query = self.generar_consulta_sql()
            df_resultado = pd.read_sql(sql_query, cnxn)
            cnxn.close()
            
            if df_resultado.empty:
                raise Exception("La consulta no devolvió datos")
            
            # 3. Procesar DataFrame
            df_procesado = self.procesar_dataframe(df_resultado)
            
            # 4. Exportar a CSV
            archivo_generado = self.exportar_csv(df_procesado)
            if not archivo_generado:
                raise Exception("Error al generar archivo CSV")
            
            # 5. Limpiar archivos antiguos
            self.limpiar_archivos_antiguos()
            
            # 6. Resumen final
            duracion = datetime.datetime.now() - inicio
            self.logger.info("=" * 60)
            self.logger.info("✅ RESPALDO COMPLETADO EXITOSAMENTE")
            self.logger.info(f"⏱️ Duración total: {duracion.total_seconds():.2f} segundos")
            self.logger.info(f"📁 Archivo generado: {archivo_generado.name}")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error("=" * 60)
            self.logger.error(f"❌ ERROR EN RESPALDO AUTOMATIZADO: {str(e)}")
            self.logger.error(f"⏱️ Duración antes del error: {(datetime.datetime.now() - inicio).total_seconds():.2f} seg")
            self.logger.error("=" * 60)
            return False

def main():
    """Función principal para ejecución automática"""
    respaldo = RespaldoBiometrico()
    exito = respaldo.ejecutar_respaldo()
    
    # Código de salida para el sistema operativo
    sys.exit(0 if exito else 1)

if __name__ == "__main__":
    main()
