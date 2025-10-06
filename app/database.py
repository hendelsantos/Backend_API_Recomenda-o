# Configuração do banco de dados SQLite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

# Usar SQLite para simplicidade
DATABASE_URL = "sqlite:///./reco.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()