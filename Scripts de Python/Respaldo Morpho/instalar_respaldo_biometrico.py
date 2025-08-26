#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSTALADOR DEL SISTEMA DE RESPALDO AUTOMATIZADO
==============================================

Este script configura automáticamente el sistema de respaldo biométrico:
- Instala dependencias necesarias
- Crea estructura de directorios
- Configura programación automática (opcional)
- Ejecuta prueba inicial del sistema

Ejecutar como administrador para configuración completa.
"""

import sys
import subprocess
import os
from pathlib import Path
import datetime

def imprimir_banner():
    """Muestra el banner del instalador"""
    print("=" * 70)
    print("🔧 INSTALADOR - SISTEMA DE RESPALDO BIOMÉTRICO AUTOMATIZADO")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Objetivo: Configurar respaldos automáticos del sistema biométrico")
    print("=" * 70)

def verificar_python():
    """Verifica la versión de Python"""
    print("\n1️⃣ VERIFICANDO PYTHON...")
    version = sys.version_info
    print(f"   🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("   ❌ ERROR: Se requiere Python 3.7 o superior")
        return False
    
    print("   ✅ Versión de Python compatible")
    return True

def instalar_dependencias():
    """Instala las librerías necesarias"""
    print("\n2️⃣ INSTALANDO DEPENDENCIAS...")
    
    dependencias = [
        'pandas',
        'pyodbc',
        'pathlib',
        'openpyxl'
    ]
    
    for dep in dependencias:
        try:
            print(f"   📦 Instalando {dep}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep, '--quiet'])
            print(f"   ✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Error al instalar {dep}, puede que ya esté instalado")
    
    print("   ✅ Proceso de instalación de dependencias completado")

def crear_estructura_directorios():
    """Crea la estructura de directorios necesaria"""
    print("\n3️⃣ CREANDO ESTRUCTURA DE DIRECTORIOS...")
    
    base_dir = Path(r"C:\Users\bgacitua\Desktop\Repositorio_GitHub\Scripts de Python")
    directorios = [
        base_dir / "Respaldos_Biometrico",
        base_dir / "Logs",
        base_dir / "Configuracion"
    ]
    
    for directorio in directorios:
        try:
            directorio.mkdir(parents=True, exist_ok=True)
            print(f"   📁 {directorio.name}: ✅ Creado/Verificado")
        except Exception as e:
            print(f"   📁 {directorio.name}: ❌ Error - {str(e)}")
    
    print("   ✅ Estructura de directorios configurada")

def verificar_conexion_bd():
    """Verifica la conexión a la base de datos"""
    print("\n4️⃣ VERIFICANDO CONEXIÓN A BASE DE DATOS...")
    
    try:
        import pyodbc
        
        # Configuración de conexión
        SERVER = '192.9.200.84'
        DATABASE = 'MorphoManager'
        USERNAME = 'rrhh_morpho'
        PASSWORD = 'PQ90@ZT*'
        
        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            f'PWD={PASSWORD};'
            'TrustServerCertificate=yes;'
        )
        
        print("   🔌 Intentando conectar...")
        cnxn = pyodbc.connect(connection_string)
        cnxn.close()
        
        print("   ✅ Conexión a SQL Server exitosa")
        print(f"   🏢 Servidor: {SERVER}")
        print(f"   🗄️ Base de datos: {DATABASE}")
        return True
        
    except ImportError:
        print("   ❌ Error: pyodbc no está instalado")
        return False
    except pyodbc.Error as e:
        print(f"   ❌ Error de conexión: {str(e)}")
        print("   💡 Verifique credenciales y conectividad de red")
        return False

def crear_archivo_prueba():
    """Crea un archivo de prueba del sistema"""
    print("\n5️⃣ EJECUTANDO PRUEBA DEL SISTEMA...")
    
    try:
        # Importar el sistema de respaldo
        sys.path.append(str(Path(__file__).parent))
        from respaldo_biometrico_automatizado import RespaldoBiometrico
        
        print("   🧪 Inicializando sistema de respaldo...")
        respaldo = RespaldoBiometrico()
        
        print("   🧪 Ejecutando respaldo de prueba...")
        exito = respaldo.ejecutar_respaldo()
        
        if exito:
            print("   ✅ Prueba ejecutada exitosamente")
            print("   📁 Verifique la carpeta 'Respaldos_Biometrico' para el archivo generado")
            return True
        else:
            print("   ❌ Error en la prueba del sistema")
            return False
            
    except ImportError as e:
        print(f"   ❌ Error al importar módulo: {str(e)}")
        print("   💡 Asegúrese de que 'respaldo_biometrico_automatizado.py' esté en la misma carpeta")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado en prueba: {str(e)}")
        return False

def crear_script_programacion():
    """Crea script para programación en Windows"""
    print("\n6️⃣ CREANDO SCRIPT DE PROGRAMACIÓN...")
    
    base_dir = Path(r"C:\Users\bgacitua\Desktop\Repositorio_GitHub\Scripts de Python")
    script_path = base_dir / "ejecutar_respaldo_biometrico.bat"
    
    contenido_bat = f"""@echo off
REM Script para ejecutar respaldo biométrico automatizado
REM Creado automáticamente por el instalador

echo ========================================
echo EJECUTANDO RESPALDO BIOMETRICO AUTOMATIZADO
echo ========================================
echo Fecha: %date% %time%
echo ========================================

cd /d "{base_dir}"
python "respaldo_biometrico_automatizado.py"

echo ========================================
echo RESPALDO COMPLETADO
echo ========================================
pause
"""
    
    try:
        script_path.write_text(contenido_bat, encoding='utf-8')
        print(f"   📄 Script creado: {script_path}")
        print("   💡 Use este archivo para programar tareas automáticas en Windows")
        
        # Instrucciones de programación
        print("\n   📋 INSTRUCCIONES PARA PROGRAMACIÓN AUTOMÁTICA:")
        print("   1. Abra 'Programador de tareas' de Windows")
        print("   2. Cree una nueva tarea básica")
        print("   3. Configure para ejecutar diariamente a las 23:30")
        print(f"   4. Seleccione el archivo: {script_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error al crear script: {str(e)}")
        return False

def mostrar_resumen_instalacion():
    """Muestra el resumen de la instalación"""
    print("\n" + "=" * 70)
    print("📋 RESUMEN DE INSTALACIÓN")
    print("=" * 70)
    
    base_dir = Path(r"C:\Users\bgacitua\Desktop\Repositorio_GitHub\Scripts de Python")
    
    archivos_esperados = [
        "respaldo_biometrico_automatizado.py",
        "config_respaldo_biometrico.conf",
        "ejecutar_respaldo_biometrico.bat"
    ]
    
    print("\n📁 ARCHIVOS DEL SISTEMA:")
    for archivo in archivos_esperados:
        ruta = base_dir / archivo
        if ruta.exists():
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
    
    print("\n📁 DIRECTORIOS:")
    directorios = ["Respaldos_Biometrico", "Logs"]
    for directorio in directorios:
        ruta = base_dir / directorio
        if ruta.exists():
            print(f"   ✅ {directorio}/")
        else:
            print(f"   ❌ {directorio}/ - NO ENCONTRADO")
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("   1. Configure la programación automática usando el archivo .bat")
    print("   2. Verifique que los respaldos se generen correctamente")
    print("   3. Revise los logs en la carpeta 'Logs' para monitoreo")
    print("   4. Ajuste la configuración en 'config_respaldo_biometrico.conf' si es necesario")
    
    print("\n📞 SOPORTE:")
    print("   - Los logs se guardan en la carpeta 'Logs'")
    print("   - Los respaldos se almacenan en 'Respaldos_Biometrico'")
    print("   - Para cambios de configuración, edite el archivo .conf")

def main():
    """Función principal del instalador"""
    imprimir_banner()
    
    pasos_completados = 0
    total_pasos = 6
    
    # Ejecutar pasos de instalación
    if verificar_python():
        pasos_completados += 1
    
    instalar_dependencias()
    pasos_completados += 1
    
    crear_estructura_directorios()
    pasos_completados += 1
    
    if verificar_conexion_bd():
        pasos_completados += 1
    
    if crear_archivo_prueba():
        pasos_completados += 1
    
    if crear_script_programacion():
        pasos_completados += 1
    
    # Mostrar resumen
    mostrar_resumen_instalacion()
    
    # Resultado final
    print("\n" + "=" * 70)
    if pasos_completados == total_pasos:
        print("✅ INSTALACIÓN COMPLETADA EXITOSAMENTE")
        print(f"📊 {pasos_completados}/{total_pasos} pasos completados")
        print("🚀 El sistema está listo para funcionar automáticamente")
    else:
        print("⚠️ INSTALACIÓN COMPLETADA CON ADVERTENCIAS")
        print(f"📊 {pasos_completados}/{total_pasos} pasos completados")
        print("💡 Revise los errores anteriores y configure manualmente si es necesario")
    
    print("=" * 70)
    
    input("\nPresione ENTER para finalizar...")

if __name__ == "__main__":
    main()
