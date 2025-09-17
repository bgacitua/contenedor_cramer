import pymysql

DEFAULT_CONFIG = {
    'host': '192.168.245.33',
    'user': 'rrhh_master',
    'password': '_Cramer2025_',
    'database': 'rrhh_app',
    'charset': 'utf8mb4'
}

try:
    connection = pymysql.connect(**DEFAULT_CONFIG)
    print("Conexión a la base de datos exitosa!")
    connection.close()
except pymysql.MySQLError as e:
    print(f"Error de conexión: {e}")