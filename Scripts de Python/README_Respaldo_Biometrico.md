# 📊 Sistema de Respaldo Automatizado Biométrico

## 🎯 Descripción
Sistema automatizado para generar "fotografías diarias" del sistema biométrico MorphoManager, generando respaldos CSV sin intervención manual.

## 🚀 Características
- ✅ **Automatización completa**: Sin intervención manual
- 📅 **Ejecución programada**: Diaria, semanal o personalizada
- 📊 **Respaldo en CSV**: Formato estándar compatible
- 🔄 **Rotación automática**: Elimina archivos antiguos
- 📝 **Sistema de logging**: Monitoreo completo
- ⚙️ **Configuración flexible**: Archivo de configuración externo
- 🛡️ **Manejo de errores**: Robusto y confiable

## 📁 Estructura de Archivos

```
Scripts de Python/
├── 📄 respaldo_biometrico_automatizado.py  # Script principal
├── ⚙️ config_respaldo_biometrico.conf       # Configuración
├── 🔧 instalar_respaldo_biometrico.py      # Instalador automático
├── 🦇 ejecutar_respaldo_biometrico.bat     # Script Windows
├── 📋 README_Respaldo_Biometrico.md        # Documentación
├── 📁 Respaldos_Biometrico/                # Archivos CSV generados
├── 📁 Logs/                                # Archivos de log
└── 📁 Configuracion/                       # Configuraciones adicionales
```

## ⚡ Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)
```powershell
# Ejecutar el instalador
python instalar_respaldo_biometrico.py
```

### Opción 2: Instalación Manual
1. **Instalar dependencias:**
```powershell
pip install pandas pyodbc pathlib openpyxl
```

2. **Crear directorios:**
```powershell
mkdir "Respaldos_Biometrico"
mkdir "Logs" 
mkdir "Configuracion"
```

3. **Configurar credenciales en el archivo de configuración**

## 🔧 Configuración

### Base de Datos
Editar `config_respaldo_biometrico.conf`:
```ini
[BASE_DE_DATOS]
SERVER = 192.9.200.84
DATABASE = MorphoManager
USERNAME = rrhh_morpho
PASSWORD = PQ90@ZT*
```

### Directorios
```ini
[DIRECTORIOS]
BASE_DIR = C:\Users\bgacitua\Desktop\Repositorio_GitHub\Scripts de Python
RESPALDOS_DIR = Respaldos_Biometrico
LOGS_DIR = Logs
```

## 🖥️ Uso

### Ejecución Manual
```powershell
# Ejecutar una sola vez
python respaldo_biometrico_automatizado.py

# O usar el script de Windows
ejecutar_respaldo_biometrico.bat
```

### Programación Automática en Windows

1. **Abrir Programador de Tareas:**
   - `Win + R` → `taskschd.msc`

2. **Crear Tarea Básica:**
   - Nombre: "Respaldo Biométrico Diario"
   - Descripción: "Respaldo automático sistema biométrico"

3. **Configurar Programación:**
   - Frecuencia: Diario
   - Hora: 23:30 (recomendada)

4. **Configurar Acción:**
   - Acción: Iniciar programa
   - Programa: `C:\Users\bgacitua\Desktop\Repositorio_GitHub\Scripts de Python\ejecutar_respaldo_biometrico.bat`

## 📊 Estructura del Respaldo CSV

### Columnas Incluidas:
- **Identificación:** `FIRSTNAME`, `LASTNAME`, `EMPLOYEEID`
- **Fecha:** `FECHA_SANTIAGO` 
- **Marcaciones:** `KEY_IN`, `KEY_OUT`, `NO_KEY`
- **Estado:** `ESTADO_ASISTENCIA` (Asiste/Ausente)
- **Estadísticas:** `CANTIDAD_DISPOSITIVOS`, `TOTAL_REGISTROS`
- **Horarios:** `PRIMERA_MARCA`, `ULTIMA_MARCA`
- **Metadatos:** `TIMESTAMP_RESPALDO`, `TIPO_RESPALDO`
- **Búsqueda:** `BusquedaRUT` (EMPLOYEEID;FECHA)

### Ejemplo de Registro:
```csv
FIRSTNAME;LASTNAME;EMPLOYEEID;FECHA_SANTIAGO;KEY_IN;KEY_OUT;NO_KEY;ESTADO_ASISTENCIA;PRIMERA_MARCA;ULTIMA_MARCA
Juan;Pérez;12345678;2025-08-20;2;2;0;Asiste;08:30:00;18:15:00
```

## 📝 Sistema de Logging

### Ubicación de Logs:
```
Logs/respaldo_biometrico_YYYYMM.log
```

### Nivel de Detalle:
- ✅ **INFO**: Operaciones exitosas
- ⚠️ **WARNING**: Advertencias menores  
- ❌ **ERROR**: Errores críticos

### Ejemplo de Log:
```
2025-08-20 23:30:01 - INFO - 🚀 INICIANDO RESPALDO AUTOMATIZADO BIOMÉTRICO
2025-08-20 23:30:02 - INFO - ✅ Conexión a SQL Server establecida exitosamente
2025-08-20 23:30:15 - INFO - 🔧 Procesando DataFrame...
2025-08-20 23:30:16 - INFO - ✅ RESPALDO CSV GENERADO EXITOSAMENTE
2025-08-20 23:30:16 - INFO - 📁 Archivo: Respaldo_Morpho_AccessLog_20250820_233016.csv
```

## 🔄 Mantenimiento Automático

### Limpieza de Archivos:
- **Respaldos antiguos:** Se eliminan automáticamente después de 30 días
- **Logs mensuales:** Se rotan cada mes
- **Configuración:** Ajustable en el archivo de configuración

## 🚨 Solución de Problemas

### Errores Comunes:

#### 1. Error de Conexión a BD
```
❌ Error al conectar a SQL Server: [28000]
```
**Solución:** Verificar credenciales y conectividad de red

#### 2. Error de Permisos
```
❌ Error al exportar CSV: [Errno 13] Permission denied
```
**Solución:** Ejecutar como administrador o verificar permisos de carpeta

#### 3. Dependencias Faltantes
```
ModuleNotFoundError: No module named 'pyodbc'
```
**Solución:** Ejecutar `pip install pyodbc pandas`

### Verificación de Estado:
```powershell
# Ver últimos logs
type "Logs\respaldo_biometrico_*.log" | findstr "ERROR"

# Verificar archivos generados
dir "Respaldos_Biometrico\*.csv" /O:D
```

## 📈 Monitoreo y Estadísticas

### Información de Respaldo:
- **Empleados únicos por respaldo**
- **Rango de fechas procesadas**
- **Cantidad de asistencias vs ausencias**
- **Tiempo de ejecución**
- **Tamaño de archivo generado**

### Métricas de Rendimiento:
- **Tiempo promedio:** 15-30 segundos
- **Tamaño típico:** 500KB - 2MB por mes
- **Registros típicos:** 5,000 - 50,000 por mes

## ⚙️ Personalización Avanzada

### Modificar Consulta SQL:
Editar la función `generar_consulta_sql()` en `respaldo_biometrico_automatizado.py`

### Cambiar Formato de Archivo:
```python
# En función exportar_csv()
df.to_excel(nombre_archivo, index=False)  # Para Excel
df.to_json(nombre_archivo, orient='records')  # Para JSON
```

### Configurar Notificaciones:
Agregar código de envío de email en la función `ejecutar_respaldo()`

## 📞 Soporte y Contacto

### Archivos de Diagnóstico:
- **Logs:** `Logs/respaldo_biometrico_YYYYMM.log`
- **Configuración:** `config_respaldo_biometrico.conf`
- **Última ejecución:** Verificar timestamp en logs

### Información del Sistema:
- **Versión Python:** 3.7+
- **Base de datos:** SQL Server (MorphoManager)
- **Sistema operativo:** Windows 10/11
- **Dependencias:** pandas, pyodbc, pathlib, openpyxl

## 📄 Changelog

### Versión 1.0 (2025-08-20)
- ✅ Sistema completo de respaldo automatizado
- ✅ Configuración flexible con archivo .conf
- ✅ Sistema de logging robusto
- ✅ Instalador automático
- ✅ Programación para Windows Task Scheduler
- ✅ Limpieza automática de archivos antiguos
- ✅ Manejo completo de errores

---

*Sistema desarrollado para automatizar el respaldo diario del sistema biométrico MorphoManager*
