from sqlalchemy.orm import Session
from models.buk_models import YourModel  # Importa tu modelo específico
import pandas as pd

def process_data(df: pd.DataFrame, db: Session):
    """
    Procesa y transforma los datos extraídos antes de enviarlos a la base de datos.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos extraídos.
        db (Session): Sesión de la base de datos para realizar operaciones.

    Returns:
        None
    """
    for index, row in df.iterrows():
        # Aquí puedes realizar cualquier transformación necesaria en los datos
        # Por ejemplo, puedes crear una instancia de tu modelo y asignar valores
        record = YourModel(
            field1=row['field1'],
            field2=row['field2'],
            # Asigna otros campos según tu modelo
        )
        
        # Agregar el registro a la sesión
        db.add(record)
    
    # Guardar los cambios en la base de datos
    db.commit()