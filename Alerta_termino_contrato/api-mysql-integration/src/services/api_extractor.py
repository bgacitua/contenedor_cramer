from datetime import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import SessionLocal
from models.buk_models import YourModel  # Importa tu modelo específico aquí

class APIExtractor:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def fetch_data(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        return response.json()

    def extract_and_store(self, endpoint, params=None):
        data = self.fetch_data(endpoint, params)
        records = data.get("data", [])
        
        if records:
            self.store_data(records)

    def store_data(self, records):
        session = SessionLocal()
        try:
            for record in records:
                # Aquí debes mapear los campos del registro a tu modelo
                new_record = YourModel(**record)  # Ajusta según tu modelo
                session.add(new_record)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error al almacenar datos: {e}")
        finally:
            session.close()

# Ejemplo de uso
if __name__ == "__main__":
    base_url = "https://cramer.buk.cl/api/v1/chile"
    headers = {
        "auth_token": "YOUR_TOKEN",  # Reemplaza con tu token
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    extractor = APIExtractor(base_url, headers)
    extractor.extract_and_store("/absences/absence", {"from": "2025-05-01", "to": "2025-08-25"})  # Ajusta el endpoint y parámetros según sea necesario