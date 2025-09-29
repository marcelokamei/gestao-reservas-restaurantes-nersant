from abc import ABC, abstractmethod
from typing import List, Optional, Any
from sqlalchemy.orm import Session
from database.connection import db_manager
import logging

logger = logging.getLogger(__name__)


class BaseRepository(ABC):
    """Classe base para repositórios com operações CRUD genéricas"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def create(self, obj: Any) -> Optional[Any]:
        """Cria um novo registro"""
        session = db_manager.get_session()
        try:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating {self.model_class.__name__}: {e}")
            return None
        finally:
            db_manager.close_session(session)
    
    def get_by_id(self, id: int) -> Optional[Any]:
        """Busca um registro por ID"""
        session = db_manager.get_session()
        try:
            return session.query(self.model_class).filter(self.model_class.id == id).first()
        except Exception as e:
            logger.error(f"Error getting {self.model_class.__name__} by id {id}: {e}")
            return None
        finally:
            db_manager.close_session(session)
    
    def get_all(self, active_only: bool = True) -> List[Any]:
        """Busca todos os registros"""
        session = db_manager.get_session()
        try:
            query = session.query(self.model_class)
            if active_only and hasattr(self.model_class, 'ativo'):
                query = query.filter(self.model_class.ativo == True)
            return query.all()
        except Exception as e:
            logger.error(f"Error getting all {self.model_class.__name__}: {e}")
            return []
        finally:
            db_manager.close_session(session)
    
    def update(self, id: int, **kwargs) -> Optional[Any]:
        """Atualiza um registro"""
        session = db_manager.get_session()
        try:
            obj = session.query(self.model_class).filter(self.model_class.id == id).first()
            if obj:
                for key, value in kwargs.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                session.commit()
                session.refresh(obj)
                return obj
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating {self.model_class.__name__} {id}: {e}")
            return None
        finally:
            db_manager.close_session(session)
    
    def delete(self, id: int) -> bool:
        """Remove um registro (soft delete se tiver campo 'ativo')"""
        session = db_manager.get_session()
        try:
            obj = session.query(self.model_class).filter(self.model_class.id == id).first()
            if obj:
                if hasattr(obj, 'ativo'):
                    obj.ativo = False
                    session.commit()
                else:
                    session.delete(obj)
                    session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting {self.model_class.__name__} {id}: {e}")
            return False
        finally:
            db_manager.close_session(session)
    
    def count(self, active_only: bool = True) -> int:
        """Conta o número de registros"""
        session = db_manager.get_session()
        try:
            query = session.query(self.model_class)
            if active_only and hasattr(self.model_class, 'ativo'):
                query = query.filter(self.model_class.ativo == True)
            return query.count()
        except Exception as e:
            logger.error(f"Error counting {self.model_class.__name__}: {e}")
            return 0
        finally:
            db_manager.close_session(session)