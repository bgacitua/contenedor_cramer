import pytest
from src.services.api_extractor import fetch_data_from_multiple_endpoints
from src.config.settings import DATABASE_URL
from src.config.database import get_db_session
from src.models.buk_models import YourModel  # Reemplaza con el nombre de tu modelo

@pytest.fixture(scope='module')
def db_session():
    session = get_db_session()
    yield session
    session.close()

def test_fetch_data_from_api():
    fecha_inicio = "2025-05-01"
    fecha_fin = "2025-05-31"
    datos_combinados, _, _ = fetch_data_from_multiple_endpoints(fecha_inicio, fecha_fin)
    
    assert datos_combinados is not None
    assert len(datos_combinados) > 0

def test_insert_data_to_db(db_session):
    # Suponiendo que tienes un modelo llamado YourModel
    data_to_insert = {
        'field1': 'value1',
        'field2': 'value2',
        # Agrega los campos necesarios según tu modelo
    }
    
    new_record = YourModel(**data_to_insert)
    db_session.add(new_record)
    db_session.commit()
    
    # Verificar que el registro se haya insertado
    inserted_record = db_session.query(YourModel).filter_by(field1='value1').first()
    assert inserted_record is not None
    assert inserted_record.field2 == 'value2'