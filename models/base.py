from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base
import os

# Erstellen Sie den absoluten Pfad zur Datenbankdatei
database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sw_unlimited.db'))

# Definieren Sie die DATABASE_URL mit dem absoluten Pfad
DATABASE_URL = f'sqlite:///{database_path}'

def init_db():
    """
    Initialisiert die Datenbank und erstellt die Tabellen gemäß den SQLAlchemy-Modellen.
    """
    engine = create_engine(DATABASE_URL, echo=False) # debug ORM Statements
    Base.metadata.create_all(engine)
    return engine

def get_session(engine=None):
    """
    Erstellt und gibt eine sessionmaker-Instanz zurück, die an die Datenbank-Engine gebunden ist.
    """
    if engine is None:
        engine = init_db()
    Session = sessionmaker(bind=engine)
    return scoped_session(Session)