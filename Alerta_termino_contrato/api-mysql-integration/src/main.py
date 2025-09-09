import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base
from services.api_extractor import fetch_data_from_multiple_endpoints
from services.data_processor import process_data
from services.database_service import save_data_to_database
from config.settings import DATABASE_URL

def main():
    # Configurar la conexión a la base de datos
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # Crear tablas si no existen
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Extraer datos de la API
        print("🚀 Iniciando la extracción de datos...")
        datos_combinados, _, _ = fetch_data_from_multiple_endpoints()

        if datos_combinados:
            # Procesar los datos extraídos
            print("🔄 Procesando datos...")
            processed_data = process_data(datos_combinados)

            # Guardar los datos en la base de datos
            print("💾 Guardando datos en la base de datos...")
            save_data_to_database(session, processed_data)
            print("✅ Datos guardados exitosamente.")
        else:
            print("❌ No se encontraron datos para guardar.")

    except Exception as e:
        print(f"💥 Error inesperado: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()