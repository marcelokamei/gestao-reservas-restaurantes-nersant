from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Cliente(Base):
    """Modelo para clientes do sistema"""
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    reservas = relationship("Reserva", back_populates="cliente")
    
    def __init__(self, nome: str, email: str, telefone: str):
        self.nome = nome
        self.email = email
        self.telefone = telefone
    
    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', email='{self.email}')>"
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro,
            'ativo': self.ativo
        }


class Restaurante(Base):
    """Modelo para restaurantes"""
    __tablename__ = 'restaurantes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(Text, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100))
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    ambientes = relationship("Ambiente", back_populates="restaurante", cascade="all, delete-orphan")
    
    def __init__(self, nome: str, endereco: str, telefone: str, email: str = None, descricao: str = None):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.descricao = descricao
    
    def __repr__(self):
        return f"<Restaurante(id={self.id}, nome='{self.nome}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone,
            'email': self.email,
            'descricao': self.descricao,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro
        }


class Ambiente(Base):
    """Modelo para ambientes/salas dos restaurantes"""
    __tablename__ = 'ambientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(Text)
    restaurante_id = Column(Integer, ForeignKey('restaurantes.id'), nullable=False)
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    restaurante = relationship("Restaurante", back_populates="ambientes")
    mesas = relationship("Mesa", back_populates="ambiente", cascade="all, delete-orphan")
    
    def __init__(self, nome: str, restaurante_id: int, descricao: str = None):
        self.nome = nome
        self.restaurante_id = restaurante_id
        self.descricao = descricao
    
    def __repr__(self):
        return f"<Ambiente(id={self.id}, nome='{self.nome}', restaurante_id={self.restaurante_id})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'restaurante_id': self.restaurante_id,
            'ativo': self.ativo
        }


class Mesa(Base):
    """Modelo para mesas dos restaurantes"""
    __tablename__ = 'mesas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String(10), nullable=False)
    capacidade = Column(Integer, nullable=False)
    ambiente_id = Column(Integer, ForeignKey('ambientes.id'), nullable=False)
    ativo = Column(Boolean, default=True)
    observacoes = Column(Text)
    
    # Relacionamentos
    ambiente = relationship("Ambiente", back_populates="mesas")
    reservas = relationship("Reserva", back_populates="mesa")
    
    def __init__(self, numero: str, capacidade: int, ambiente_id: int, observacoes: str = None):
        self.numero = numero
        self.capacidade = capacidade
        self.ambiente_id = ambiente_id
        self.observacoes = observacoes
    
    def __repr__(self):
        return f"<Mesa(id={self.id}, numero='{self.numero}', capacidade={self.capacidade})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'capacidade': self.capacidade,
            'ambiente_id': self.ambiente_id,
            'ativo': self.ativo,
            'observacoes': self.observacoes
        }


class Reserva(Base):
    """Modelo para reservas de mesas"""
    __tablename__ = 'reservas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    mesa_id = Column(Integer, ForeignKey('mesas.id'), nullable=False)
    data_reserva = Column(DateTime, nullable=False)
    numero_pessoas = Column(Integer, nullable=False)
    observacoes = Column(Text)
    status = Column(String(20), default='confirmada')  # confirmada, cancelada, finalizada
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="reservas")
    mesa = relationship("Mesa", back_populates="reservas")
    
    def __init__(self, cliente_id: int, mesa_id: int, data_reserva: datetime, 
                 numero_pessoas: int, observacoes: str = None):
        self.cliente_id = cliente_id
        self.mesa_id = mesa_id
        self.data_reserva = data_reserva
        self.numero_pessoas = numero_pessoas
        self.observacoes = observacoes
    
    def __repr__(self):
        return f"<Reserva(id={self.id}, cliente_id={self.cliente_id}, mesa_id={self.mesa_id}, data={self.data_reserva})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'mesa_id': self.mesa_id,
            'data_reserva': self.data_reserva,
            'numero_pessoas': self.numero_pessoas,
            'observacoes': self.observacoes,
            'status': self.status,
            'data_criacao': self.data_criacao
        }