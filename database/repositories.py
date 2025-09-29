from typing import List, Optional
from datetime import datetime, date
from models import Cliente, Restaurante, Ambiente, Mesa, Reserva
from database.base_repository import BaseRepository
from database.connection import db_manager
import logging

logger = logging.getLogger(__name__)


class ClienteRepository(BaseRepository):
    """Repositório para operações com clientes"""
    
    def __init__(self):
        super().__init__(Cliente)
    
    def get_by_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        session = db_manager.get_session()
        try:
            return session.query(Cliente).filter(Cliente.email == email).first()
        except Exception as e:
            logger.error(f"Error getting client by email {email}: {e}")
            return None
        finally:
            db_manager.close_session(session)


class RestauranteRepository(BaseRepository):
    """Repositório para operações com restaurantes"""
    
    def __init__(self):
        super().__init__(Restaurante)
    
    def get_with_ambientes(self, restaurante_id: int) -> Optional[Restaurante]:
        """Busca restaurante com seus ambientes"""
        session = db_manager.get_session()
        try:
            return session.query(Restaurante).filter(
                Restaurante.id == restaurante_id,
                Restaurante.ativo == True
            ).first()
        except Exception as e:
            logger.error(f"Error getting restaurant with environments {restaurante_id}: {e}")
            return None
        finally:
            db_manager.close_session(session)


class AmbienteRepository(BaseRepository):
    """Repositório para operações com ambientes"""
    
    def __init__(self):
        super().__init__(Ambiente)
    
    def get_by_restaurante(self, restaurante_id: int) -> List[Ambiente]:
        """Busca ambientes por restaurante"""
        session = db_manager.get_session()
        try:
            return session.query(Ambiente).filter(
                Ambiente.restaurante_id == restaurante_id,
                Ambiente.ativo == True
            ).all()
        except Exception as e:
            logger.error(f"Error getting environments by restaurant {restaurante_id}: {e}")
            return []
        finally:
            db_manager.close_session(session)


class MesaRepository(BaseRepository):
    """Repositório para operações com mesas"""
    
    def __init__(self):
        super().__init__(Mesa)
    
    def get_by_ambiente(self, ambiente_id: int) -> List[Mesa]:
        """Busca mesas por ambiente"""
        session = db_manager.get_session()
        try:
            return session.query(Mesa).filter(
                Mesa.ambiente_id == ambiente_id,
                Mesa.ativo == True
            ).all()
        except Exception as e:
            logger.error(f"Error getting tables by environment {ambiente_id}: {e}")
            return []
        finally:
            db_manager.close_session(session)
    
    def get_available_tables(self, ambiente_id: int, data_reserva: datetime, 
                           numero_pessoas: int) -> List[Mesa]:
        """Busca mesas disponíveis para uma data/hora específica"""
        session = db_manager.get_session()
        try:
            # Buscar mesas do ambiente com capacidade suficiente
            mesas_ambiente = session.query(Mesa).filter(
                Mesa.ambiente_id == ambiente_id,
                Mesa.capacidade >= numero_pessoas,
                Mesa.ativo == True
            ).all()
            
            # Verificar quais mesas não têm reserva no horário solicitado
            mesas_disponiveis = []
            for mesa in mesas_ambiente:
                reserva_conflito = session.query(Reserva).filter(
                    Reserva.mesa_id == mesa.id,
                    Reserva.data_reserva == data_reserva,
                    Reserva.status == 'confirmada'
                ).first()
                
                if not reserva_conflito:
                    mesas_disponiveis.append(mesa)
            
            return mesas_disponiveis
            
        except Exception as e:
            logger.error(f"Error getting available tables: {e}")
            return []
        finally:
            db_manager.close_session(session)


class ReservaRepository(BaseRepository):
    """Repositório para operações com reservas"""
    
    def __init__(self):
        super().__init__(Reserva)
    
    def get_by_cliente(self, cliente_id: int) -> List[Reserva]:
        """Busca reservas por cliente"""
        session = db_manager.get_session()
        try:
            return session.query(Reserva).filter(
                Reserva.cliente_id == cliente_id
            ).order_by(Reserva.data_reserva.desc()).all()
        except Exception as e:
            logger.error(f"Error getting reservations by client {cliente_id}: {e}")
            return []
        finally:
            db_manager.close_session(session)
    
    def get_by_data(self, data_inicio: date, data_fim: date = None) -> List[Reserva]:
        """Busca reservas por período"""
        session = db_manager.get_session()
        try:
            if data_fim is None:
                data_fim = data_inicio
            
            return session.query(Reserva).filter(
                Reserva.data_reserva >= data_inicio,
                Reserva.data_reserva <= data_fim
            ).order_by(Reserva.data_reserva).all()
        except Exception as e:
            logger.error(f"Error getting reservations by date: {e}")
            return []
        finally:
            db_manager.close_session(session)
    
    def get_by_restaurante(self, restaurante_id: int) -> List[Reserva]:
        """Busca reservas por restaurante"""
        session = db_manager.get_session()
        try:
            return session.query(Reserva).join(Mesa).join(Ambiente).filter(
                Ambiente.restaurante_id == restaurante_id
            ).order_by(Reserva.data_reserva.desc()).all()
        except Exception as e:
            logger.error(f"Error getting reservations by restaurant {restaurante_id}: {e}")
            return []
        finally:
            db_manager.close_session(session)
    
    def cancel_reservation(self, reserva_id: int) -> bool:
        """Cancela uma reserva"""
        return self.update(reserva_id, status='cancelada')


# Instâncias dos repositórios
cliente_repo = ClienteRepository()
restaurante_repo = RestauranteRepository()
ambiente_repo = AmbienteRepository()
mesa_repo = MesaRepository()
reserva_repo = ReservaRepository()