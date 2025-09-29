from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from config import Config
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gerenciador de conexão com banco de dados"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.Session = None
    
    def initialize(self):
        """Inicializa a conexão com o banco de dados"""
        try:
            self.engine = create_engine(
                Config.DATABASE_URL,
                echo=False,  # Set to True for SQL debugging
                pool_pre_ping=True
            )
            
            self.session_factory = sessionmaker(bind=self.engine)
            self.Session = scoped_session(self.session_factory)
            
            # Criar todas as tabelas
            Base.metadata.create_all(self.engine)
            
            logger.info("Database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            return False
    
    def get_session(self):
        """Retorna uma sessão do banco de dados"""
        if self.Session is None:
            self.initialize()
        return self.Session()
    
    def close_session(self, session):
        """Fecha uma sessão do banco de dados"""
        try:
            session.close()
        except Exception as e:
            logger.error(f"Error closing session: {e}")


# Instância global do gerenciador de banco
db_manager = DatabaseManager()