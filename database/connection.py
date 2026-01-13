
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sigeem',
    'user': 'postgres',
    'password': '123',
    'port': 5432
}

# SQLAlchemy Base
Base = declarative_base()

class DatabaseConnection:
    """Classe para gerenciar conexões com o banco de dados"""
    
    _engine = None
    _session_factory = None
    
    @classmethod
    def get_engine(cls):
        """Retorna a engine do SQLAlchemy"""
        if cls._engine is None:
            connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
            cls._engine = create_engine(connection_string, echo=False)
        return cls._engine
    
    @classmethod
    def get_session(cls):
        """Retorna uma sessão do SQLAlchemy"""
        if cls._session_factory is None:
            cls._session_factory = sessionmaker(bind=cls.get_engine())
        return cls._session_factory()
    
    @classmethod
    def get_psycopg2_connection(cls):
        """Retorna uma conexão psycopg2"""
        return psycopg2.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
    
    @classmethod
    def create_tables(cls):
        """Cria todas as tabelas no banco de dados"""
        Base.metadata.create_all(cls.get_engine())