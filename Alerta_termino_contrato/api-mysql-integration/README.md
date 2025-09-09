# API MySQL Integration

Este proyecto tiene como objetivo extraer datos de una API y almacenarlos en una base de datos MySQL. A continuación se detallan las características y la estructura del proyecto.

## Estructura del Proyecto

```
api-mysql-integration
├── src
│   ├── __init__.py
│   ├── main.py                # Punto de entrada de la aplicación
│   ├── config                 # Configuración de la aplicación
│   │   ├── __init__.py
│   │   ├── database.py        # Configuración de la conexión a la base de datos
│   │   └── settings.py        # Configuración general de la aplicación
│   ├── models                 # Modelos de datos
│   │   ├── __init__.py
│   │   ├── base.py            # Clase base para los modelos de datos
│   │   └── buk_models.py      # Modelos específicos para la base de datos
│   ├── services               # Servicios de la aplicación
│   │   ├── __init__.py
│   │   ├── api_extractor.py    # Lógica para extraer datos de la API
│   │   ├── database_service.py  # Funciones para interactuar con la base de datos
│   │   └── data_processor.py    # Funciones para procesar los datos extraídos
│   └── utils                  # Utilidades de la aplicación
│       ├── __init__.py
│       ├── logger.py          # Configuración de logs
│       └── validators.py      # Funciones para validar datos
├── migrations                  # Migraciones de la base de datos
│   ├── __init__.py
│   └── create_tables.sql      # Instrucciones SQL para crear tablas
├── logs                        # Archivos de registro
├── tests                       # Pruebas unitarias
│   ├── __init__.py
│   ├── test_database.py       # Pruebas para funciones de base de datos
│   └── test_api.py           # Pruebas para funciones de extracción de API
├── requirements.txt           # Dependencias del proyecto
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos y directorios a ignorar por Git
├── setup.py                   # Configuración del paquete
└── README.md                  # Documentación del proyecto
```

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd api-mysql-integration
   ```

2. Crea un entorno virtual y actívalo:
   ```
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno en un archivo `.env` basado en el archivo `.env.example`.

## Uso

Para ejecutar la aplicación, utiliza el siguiente comando:
```
python src/main.py
```

Esto iniciará el proceso de extracción de datos desde la API y los almacenará en la base de datos MySQL configurada.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.