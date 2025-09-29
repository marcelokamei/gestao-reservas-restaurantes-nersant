from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from models import Cliente, Restaurante, Ambiente, Mesa, Reserva
from database.repositories import (
    cliente_repo, restaurante_repo, ambiente_repo, mesa_repo, reserva_repo
)
from database.connection import db_manager
from utils.validators import DataValidator, ValidationError
import logging

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """Classe base para serviços"""
    
    def __init__(self, repository):
        self.repository = repository


class ClienteService(BaseService):
    """Serviço para operações com clientes"""
    
    def __init__(self):
        super().__init__(cliente_repo)
    
    def create_cliente(self, nome: str, email: str, telefone: str) -> Optional[Cliente]:
        """
        Cria um novo cliente
        
        Args:
            nome: Nome do cliente
            email: Email do cliente
            telefone: Telefone do cliente
            
        Returns:
            Cliente criado ou None se houver erro
        """
        try:
            # Validações
            is_valid, message = DataValidator.validate_name(nome)
            if not is_valid:
                raise ValidationError(message)
            
            is_valid, message = DataValidator.validate_email(email)
            if not is_valid:
                raise ValidationError(message)
            
            is_valid, message = DataValidator.validate_phone(telefone)
            if not is_valid:
                raise ValidationError(message)
            
            # Verificar se email já existe
            existing_client = self.repository.get_by_email(email)
            if existing_client:
                raise ValidationError("Email já cadastrado")
            
            # Criar cliente
            cliente = Cliente(nome=nome.strip(), email=email.strip().lower(), telefone=telefone.strip())
            return self.repository.create(cliente)
            
        except ValidationError as e:
            logger.error(f"Validation error creating client: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error creating client: {e}")
            return None
    
    def get_cliente_by_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        return self.repository.get_by_email(email.strip().lower())
    
    def get_cliente_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca cliente por ID"""
        return self.repository.get_by_id(cliente_id)
    
    def get_all_clientes(self) -> List[Cliente]:
        """Retorna todos os clientes ativos"""
        return self.repository.get_all()
    
    def update_cliente(self, cliente_id: int, **kwargs) -> Optional[Cliente]:
        """Atualiza dados do cliente"""
        try:
            # Validar dados se fornecidos
            if 'nome' in kwargs:
                is_valid, message = DataValidator.validate_name(kwargs['nome'])
                if not is_valid:
                    raise ValidationError(message)
                kwargs['nome'] = kwargs['nome'].strip()
            
            if 'email' in kwargs:
                is_valid, message = DataValidator.validate_email(kwargs['email'])
                if not is_valid:
                    raise ValidationError(message)
                kwargs['email'] = kwargs['email'].strip().lower()
                
                # Verificar se email já existe em outro cliente
                existing_client = self.repository.get_by_email(kwargs['email'])
                if existing_client and existing_client.id != cliente_id:
                    raise ValidationError("Email já cadastrado por outro cliente")
            
            if 'telefone' in kwargs:
                is_valid, message = DataValidator.validate_phone(kwargs['telefone'])
                if not is_valid:
                    raise ValidationError(message)
                kwargs['telefone'] = kwargs['telefone'].strip()
            
            return self.repository.update(cliente_id, **kwargs)
            
        except ValidationError as e:
            logger.error(f"Validation error updating client: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error updating client: {e}")
            return None
    
    def update_cliente_dados(self, cliente_id: int, nome: str, email: str, telefone: str) -> Optional[Cliente]:
        """
        Atualiza dados do cliente com parâmetros específicos
        
        Args:
            cliente_id: ID do cliente
            nome: Novo nome
            email: Novo email
            telefone: Novo telefone
            
        Returns:
            Cliente atualizado ou None se houver erro
        """
        return self.update_cliente(cliente_id, nome=nome, email=email, telefone=telefone)
    
    def delete_cliente(self, cliente_id: int) -> bool:
        """Remove cliente (soft delete)"""
        return self.repository.delete(cliente_id)


class RestauranteService(BaseService):
    """Serviço para operações com restaurantes"""
    
    def __init__(self):
        super().__init__(restaurante_repo)
    
    def create_restaurante(self, nome: str, endereco: str, telefone: str, 
                          email: str = None, descricao: str = None) -> Optional[Restaurante]:
        """
        Cria um novo restaurante
        
        Args:
            nome: Nome do restaurante
            endereco: Endereço do restaurante
            telefone: Telefone do restaurante
            email: Email do restaurante (opcional)
            descricao: Descrição do restaurante (opcional)
            
        Returns:
            Restaurante criado ou None se houver erro
        """
        try:
            # Validações
            is_valid, message = DataValidator.validate_name(nome)
            if not is_valid:
                raise ValidationError(message)
            
            if not endereco or not endereco.strip():
                raise ValidationError("Morada é obrigatória")
            
            is_valid, message = DataValidator.validate_phone(telefone)
            if not is_valid:
                raise ValidationError(message)
            
            if email:
                is_valid, message = DataValidator.validate_email(email)
                if not is_valid:
                    raise ValidationError(message)
                email = email.strip().lower()
            
            # Criar restaurante
            restaurante = Restaurante(
                nome=nome.strip(),
                endereco=endereco.strip(),
                telefone=telefone.strip(),
                email=email,
                descricao=descricao.strip() if descricao else None
            )
            return self.repository.create(restaurante)
            
        except ValidationError as e:
            logger.error(f"Validation error creating restaurant: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error creating restaurant: {e}")
            return None
    
    def get_all_restaurantes(self) -> List[Restaurante]:
        """Retorna todos os restaurantes ativos"""
        return self.repository.get_all()
    
    def get_restaurante_by_id(self, restaurante_id: int) -> Optional[Restaurante]:
        """Busca restaurante por ID"""
        return self.repository.get_by_id(restaurante_id)
    
    def update_restaurante(self, restaurante_id: int, **kwargs) -> Optional[Restaurante]:
        """Atualiza dados do restaurante"""
        try:
            # Validações similares ao create
            if 'nome' in kwargs:
                is_valid, message = DataValidator.validate_name(kwargs['nome'])
                if not is_valid:
                    raise ValidationError(message)
                kwargs['nome'] = kwargs['nome'].strip()
            
            if 'telefone' in kwargs:
                is_valid, message = DataValidator.validate_phone(kwargs['telefone'])
                if not is_valid:
                    raise ValidationError(message)
                kwargs['telefone'] = kwargs['telefone'].strip()
            
            if 'email' in kwargs and kwargs['email']:
                is_valid, message = DataValidator.validate_email(kwargs['email'])
                if not is_valid:
                    raise ValidationError(message)
                kwargs['email'] = kwargs['email'].strip().lower()
            
            return self.repository.update(restaurante_id, **kwargs)
            
        except ValidationError as e:
            logger.error(f"Validation error updating restaurant: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error updating restaurant: {e}")
            return None
    
    def delete_restaurante(self, restaurante_id: int) -> bool:
        """Remove restaurante (soft delete)"""
        return self.repository.delete(restaurante_id)


class AmbienteService(BaseService):
    """Serviço para operações com ambientes"""
    
    def __init__(self):
        super().__init__(ambiente_repo)
    
    def create_ambiente(self, nome: str, restaurante_id: int, descricao: str = None) -> Optional[Ambiente]:
        """
        Cria um novo ambiente
        
        Args:
            nome: Nome do ambiente
            restaurante_id: ID do restaurante
            descricao: Descrição do ambiente (opcional)
            
        Returns:
            Ambiente criado ou None se houver erro
        """
        try:
            # Validações
            if not nome or not nome.strip():
                raise ValidationError("Nome do ambiente é obrigatório")
            
            if not restaurante_id:
                raise ValidationError("Restaurante é obrigatório")
            
            # Verificar se restaurante existe
            restaurante = restaurante_repo.get_by_id(restaurante_id)
            if not restaurante:
                raise ValidationError("Restaurante não encontrado")
            
            # Criar ambiente
            ambiente = Ambiente(
                nome=nome.strip(),
                restaurante_id=restaurante_id,
                descricao=descricao.strip() if descricao else None
            )
            return self.repository.create(ambiente)
            
        except ValidationError as e:
            logger.error(f"Validation error creating environment: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error creating environment: {e}")
            return None
    
    def get_ambientes_by_restaurante(self, restaurante_id: int) -> List[Ambiente]:
        """Busca ambientes por restaurante"""
        return self.repository.get_by_restaurante(restaurante_id)
    
    def get_ambiente_by_id(self, ambiente_id: int) -> Optional[Ambiente]:
        """Busca ambiente por ID"""
        return self.repository.get_by_id(ambiente_id)
    
    def update_ambiente(self, ambiente_id: int, **kwargs) -> Optional[Ambiente]:
        """Atualiza dados do ambiente"""
        try:
            if 'nome' in kwargs:
                if not kwargs['nome'] or not kwargs['nome'].strip():
                    raise ValidationError("Nome do ambiente é obrigatório")
                kwargs['nome'] = kwargs['nome'].strip()
            
            return self.repository.update(ambiente_id, **kwargs)
            
        except ValidationError as e:
            logger.error(f"Validation error updating environment: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error updating environment: {e}")
            return None
    
    def delete_ambiente(self, ambiente_id: int) -> bool:
        """Remove ambiente (soft delete)"""
        return self.repository.delete(ambiente_id)


class MesaService(BaseService):
    """Serviço para operações com mesas"""
    
    def __init__(self):
        super().__init__(mesa_repo)
    
    def create_mesa(self, numero: str, capacidade: int, ambiente_id: int, 
                   observacoes: str = None) -> Optional[Mesa]:
        """
        Cria uma nova mesa
        
        Args:
            numero: Número da mesa
            capacidade: Capacidade da mesa
            ambiente_id: ID do ambiente
            observacoes: Observações sobre a mesa (opcional)
            
        Returns:
            Mesa criada ou None se houver erro
        """
        try:
            # Validações
            is_valid, message = DataValidator.validate_table_number(numero)
            if not is_valid:
                raise ValidationError(message)
            
            is_valid, message = DataValidator.validate_capacity(capacidade)
            if not is_valid:
                raise ValidationError(message)
            
            if not ambiente_id:
                raise ValidationError("Ambiente é obrigatório")
            
            # Verificar se ambiente existe
            ambiente = ambiente_repo.get_by_id(ambiente_id)
            if not ambiente:
                raise ValidationError("Ambiente não encontrado")
            
            # Criar mesa
            mesa = Mesa(
                numero=numero.strip(),
                capacidade=capacidade,
                ambiente_id=ambiente_id,
                observacoes=observacoes.strip() if observacoes else None
            )
            return self.repository.create(mesa)
            
        except ValidationError as e:
            logger.error(f"Validation error creating table: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            return None
    
    def get_mesas_by_ambiente(self, ambiente_id: int) -> List[Mesa]:
        """Busca mesas por ambiente"""
        return self.repository.get_by_ambiente(ambiente_id)
    
    def get_mesa_by_id(self, mesa_id: int) -> Optional[Mesa]:
        """Busca mesa por ID"""
        return self.repository.get_by_id(mesa_id)
    
    def get_available_tables(self, ambiente_id: int, data_reserva: datetime, 
                           numero_pessoas: int) -> List[Mesa]:
        """Busca mesas disponíveis"""
        return self.repository.get_available_tables(ambiente_id, data_reserva, numero_pessoas)
    
    def update_mesa(self, mesa_id: int, **kwargs) -> Optional[Mesa]:
        """Atualiza dados da mesa"""
        try:
            if 'numero' in kwargs:
                is_valid, message = DataValidator.validate_table_number(kwargs['numero'])
                if not is_valid:
                    raise ValidationError(message)
                kwargs['numero'] = kwargs['numero'].strip()
            
            if 'capacidade' in kwargs:
                is_valid, message = DataValidator.validate_capacity(kwargs['capacidade'])
                if not is_valid:
                    raise ValidationError(message)
            
            return self.repository.update(mesa_id, **kwargs)
            
        except ValidationError as e:
            logger.error(f"Validation error updating table: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error updating table: {e}")
            return None
    
    def delete_mesa(self, mesa_id: int) -> bool:
        """Remove mesa (soft delete)"""
        return self.repository.delete(mesa_id)


class ReservaService(BaseService):
    """Serviço para operações com reservas"""
    
    def __init__(self):
        super().__init__(reserva_repo)
    
    def create_reserva(self, cliente_id: int, mesa_id: int, data_reserva: datetime,
                      numero_pessoas: int, observacoes: str = None) -> Optional[Reserva]:
        """
        Cria uma nova reserva
        
        Args:
            cliente_id: ID do cliente
            mesa_id: ID da mesa
            data_reserva: Data e hora da reserva
            numero_pessoas: Número de pessoas
            observacoes: Observações sobre a reserva (opcional)
            
        Returns:
            Reserva criada ou None se houver erro
        """
        try:
            # Validações
            if not cliente_id:
                raise ValidationError("Cliente é obrigatório")
            
            if not mesa_id:
                raise ValidationError("Mesa é obrigatória")
            
            is_valid, message = DataValidator.validate_reservation_date(data_reserva)
            if not is_valid:
                raise ValidationError(message)
            
            is_valid, message = DataValidator.validate_capacity(numero_pessoas)
            if not is_valid:
                raise ValidationError(message)
            
            # Verificar se cliente existe
            cliente = cliente_repo.get_by_id(cliente_id)
            if not cliente:
                raise ValidationError("Cliente não encontrado")
            
            # Verificar se mesa existe
            mesa = mesa_repo.get_by_id(mesa_id)
            if not mesa:
                raise ValidationError("Mesa não encontrada")
            
            # Verificar capacidade da mesa
            if numero_pessoas > mesa.capacidade:
                raise ValidationError(f"Mesa comporta apenas {mesa.capacidade} pessoas")
            
            # Verificar disponibilidade da mesa
            session = db_manager.get_session()
            try:
                reserva_existente = session.query(Reserva).filter(
                    Reserva.mesa_id == mesa_id,
                    Reserva.data_reserva == data_reserva,
                    Reserva.status == 'confirmada'
                ).first()
                
                if reserva_existente:
                    raise ValidationError("Mesa já reservada para este horário")
            finally:
                db_manager.close_session(session)
            
            # Criar reserva
            reserva = Reserva(
                cliente_id=cliente_id,
                mesa_id=mesa_id,
                data_reserva=data_reserva,
                numero_pessoas=numero_pessoas,
                observacoes=observacoes.strip() if observacoes else None
            )
            return self.repository.create(reserva)
            
        except ValidationError as e:
            logger.error(f"Validation error creating reservation: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error creating reservation: {e}")
            return None
    
    def get_reservas_by_cliente(self, cliente_id: int) -> List[Reserva]:
        """Busca reservas por cliente"""
        return self.repository.get_by_cliente(cliente_id)
    
    def get_reservas_by_restaurante(self, restaurante_id: int) -> List[Reserva]:
        """Busca reservas por restaurante"""
        return self.repository.get_by_restaurante(restaurante_id)
    
    def get_reserva_by_id(self, reserva_id: int) -> Optional[Reserva]:
        """Busca reserva por ID"""
        return self.repository.get_by_id(reserva_id)
    
    def cancel_reserva(self, reserva_id: int) -> bool:
        """Cancela uma reserva"""
        return self.repository.cancel_reservation(reserva_id)
    
    def update_reserva(self, reserva_id: int, **kwargs) -> Optional[Reserva]:
        """Atualiza dados da reserva"""
        try:
            if 'data_reserva' in kwargs:
                is_valid, message = DataValidator.validate_reservation_date(kwargs['data_reserva'])
                if not is_valid:
                    raise ValidationError(message)
            
            if 'numero_pessoas' in kwargs:
                is_valid, message = DataValidator.validate_capacity(kwargs['numero_pessoas'])
                if not is_valid:
                    raise ValidationError(message)
                
                # Verificar capacidade da mesa se estiver mudando o número de pessoas
                reserva = self.repository.get_by_id(reserva_id)
                if reserva:
                    mesa = mesa_repo.get_by_id(reserva.mesa_id)
                    if mesa and kwargs['numero_pessoas'] > mesa.capacidade:
                        raise ValidationError(f"Mesa comporta apenas {mesa.capacidade} pessoas")
            
            return self.repository.update(reserva_id, **kwargs)
            
        except ValidationError as e:
            logger.error(f"Validation error updating reservation: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error updating reservation: {e}")
            return None

    def get_reservas_by_data(self, data: datetime) -> List[Reserva]:
        """Busca reservas por data específica"""
        try:
            session = db_manager.get_session()
            try:
                # Criar data de início e fim do dia
                start_date = data.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = data.replace(hour=23, minute=59, second=59, microsecond=999999)
                
                # Buscar reservas da data específica
                reservas = session.query(Reserva).filter(
                    Reserva.data_reserva >= start_date,
                    Reserva.data_reserva <= end_date
                ).all()
                
                return reservas
            finally:
                db_manager.close_session(session)
        except Exception as e:
            logger.error(f"Error getting reservations by date: {e}")
            return []
    
    def get_all_reservas(self) -> List[Reserva]:
        """Busca todas as reservas"""
        return self.repository.get_all()
    
    def delete_reserva(self, reserva_id: int) -> bool:
        """
        Exclui uma reserva permanentemente
        
        Args:
            reserva_id: ID da reserva
            
        Returns:
            True se excluída com sucesso, False caso contrário
        """
        try:
            return self.repository.delete(reserva_id)
        except Exception as e:
            logger.error(f"Error deleting reservation: {e}")
            return False


# Instâncias dos serviços
cliente_service = ClienteService()
restaurante_service = RestauranteService()
ambiente_service = AmbienteService()
mesa_service = MesaService()
reserva_service = ReservaService()