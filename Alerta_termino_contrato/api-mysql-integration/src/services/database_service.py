from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.database import DATABASE_URL

Base = declarative_base()

class BukData(Base):
    __tablename__ = 'buk_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    field1 = Column(String(255))
    field2 = Column(String(255))
    created_at = Column(DateTime)

def get_database_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

def insert_buk_data(data):
    session = get_database_session()
    try:
        new_record = BukData(
            field1=data.get('field1'),
            field2=data.get('field2'),
            created_at=data.get('created_at')
        )
        session.add(new_record)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        session.close()

def fetch_all_buk_data():
    session = get_database_session()
    try:
        return session.query(BukData).all()
    finally:
        session.close()