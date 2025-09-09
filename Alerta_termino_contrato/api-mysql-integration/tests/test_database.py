import pytest
from src.config.database import SessionLocal, engine
from src.models.buk_models import Base

@pytest.fixture(scope='module')
def setup_database():
    # Crear las tablas en la base de datos
    Base.metadata.create_all(bind=engine)
    yield
    # Eliminar las tablas después de las pruebas
    Base.metadata.drop_all(bind=engine)

def test_database_connection(setup_database):
    # Probar la conexión a la base de datos
    db = SessionLocal()
    assert db is not None
    db.close()

# Aquí se pueden agregar más pruebas relacionadas con la base de datos.