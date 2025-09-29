"""
Script para popular o banco de dados com dados iniciais de exemplo
"""

from datetime import datetime, timedelta, time
from database.connection import db_manager
from services import (
    restaurante_service, ambiente_service, mesa_service, 
    cliente_service, reserva_service
)
from utils.validators import ValidationError
import logging

logger = logging.getLogger(__name__)


def create_sample_data():
    """Cria dados de exemplo no banco"""
    print("🔄 Criando dados de exemplo...")
    
    try:
        # Inicializar banco
        if not db_manager.initialize():
            print("❌ Erro ao inicializar banco de dados!")
            return False
        
        # 1. Criar restaurantes
        print("📍 Criando restaurantes...")
        
        restaurantes_data = [
            {
                "nome": "Bella Italiana",
                "endereco": "Rua Augusta, 123 - Chiado, Lisboa",
                "telefone": "213 456 789",
                "email": "contato@gmail.com",
                "descricao": "Autêntica culinária italiana em ambiente acolhedor"
            },
            {
                "nome": "Sushi Zen",
                "endereco": "Avenida da Liberdade, 456 - Avenidas Novas, Lisboa",
                "telefone": "212 345 678",
                "email": "sushizen@gmail.com",
                "descricao": "O melhor da culinária japonesa com ingredientes frescos"
            },
            {
                "nome": "Tasca do Porto",
                "endereco": "Rua das Flores, 789 - Ribeira, Porto",
                "telefone": "223 456 789",
                "email": "tasca@gmail.com",
                "descricao": "Tradição portuguesa com pratos típicos e ambiente familiar"
            }
        ]
        
        restaurantes = []
        for rest_data in restaurantes_data:
            restaurante = restaurante_service.create_restaurante(**rest_data)
            if restaurante:
                restaurantes.append(restaurante)
                print(f"   ✅ {restaurante.nome}")
        
        # 2. Criar ambientes
        print("🏠 Criando ambientes...")
        
        ambientes_data = [
            # Bella Italiana
            {"nome": "Salão Principal", "restaurante_id": restaurantes[0].id, "descricao": "Ambiente interior climatizado"},
            {"nome": "Esplanada", "restaurante_id": restaurantes[0].id, "descricao": "Área exterior com vista para o jardim"},
            
            # Sushi Zen
            {"nome": "Sushi Bar", "restaurante_id": restaurantes[1].id, "descricao": "Balcão em frente ao sushiman"},
            {"nome": "Salão VIP", "restaurante_id": restaurantes[1].id, "descricao": "Ambiente reservado para ocasiões especiais"},
            
            # Tasca do Porto
            {"nome": "Salão Principal", "restaurante_id": restaurantes[2].id, "descricao": "Amplo salão com decoração tradicional"},
            {"nome": "Sala Privada", "restaurante_id": restaurantes[2].id, "descricao": "Ambiente reservado para grupos"}
        ]
        
        ambientes = []
        for amb_data in ambientes_data:
            ambiente = ambiente_service.create_ambiente(**amb_data)
            if ambiente:
                ambientes.append(ambiente)
                print(f"   ✅ {ambiente.nome}")
        
        # 3. Criar mesas
        print("🪑 Criando mesas...")
        
        mesas_data = [
            # Bella Italiana - Salão Principal
            {"numero": "01", "capacidade": 2, "ambiente_id": ambientes[0].id},
            {"numero": "02", "capacidade": 4, "ambiente_id": ambientes[0].id},
            {"numero": "03", "capacidade": 6, "ambiente_id": ambientes[0].id},
            {"numero": "04", "capacidade": 4, "ambiente_id": ambientes[0].id},
            {"numero": "05", "capacidade": 2, "ambiente_id": ambientes[0].id},
            
            # Bella Italiana - Esplanada
            {"numero": "E1", "capacidade": 4, "ambiente_id": ambientes[1].id, "observacoes": "Mesa com vista para o jardim"},
            {"numero": "E2", "capacidade": 6, "ambiente_id": ambientes[1].id, "observacoes": "Mesa com vista para o jardim"},
            {"numero": "E3", "capacidade": 2, "ambiente_id": ambientes[1].id, "observacoes": "Mesa romântica"},
            
            # Sushi Zen - Sushi Bar
            {"numero": "B1", "capacidade": 2, "ambiente_id": ambientes[2].id, "observacoes": "Lugar no balcão"},
            {"numero": "B2", "capacidade": 2, "ambiente_id": ambientes[2].id, "observacoes": "Lugar no balcão"},
            {"numero": "B3", "capacidade": 2, "ambiente_id": ambientes[2].id, "observacoes": "Lugar no balcão"},
            
            # Sushi Zen - Salão VIP
            {"numero": "V1", "capacidade": 8, "ambiente_id": ambientes[3].id, "observacoes": "Mesa grande para grupos"},
            {"numero": "V2", "capacidade": 4, "ambiente_id": ambientes[3].id},
            
            # Tasca do Porto - Salão Principal
            {"numero": "P01", "capacidade": 4, "ambiente_id": ambientes[4].id},
            {"numero": "P02", "capacidade": 6, "ambiente_id": ambientes[4].id},
            {"numero": "P03", "capacidade": 8, "ambiente_id": ambientes[4].id},
            {"numero": "P04", "capacidade": 4, "ambiente_id": ambientes[4].id},
            {"numero": "P05", "capacidade": 2, "ambiente_id": ambientes[4].id},
            
            # Tasca do Porto - Sala Privada
            {"numero": "PR1", "capacidade": 12, "ambiente_id": ambientes[5].id, "observacoes": "Mesa para eventos privados"}
        ]
        
        mesas = []
        for mesa_data in mesas_data:
            mesa = mesa_service.create_mesa(**mesa_data)
            if mesa:
                mesas.append(mesa)
                print(f"   ✅ Mesa {mesa.numero}")
        
        # 4. Criar clientes
        print("👥 Criando clientes...")
        
        clientes_data = [
            {"nome": "João Silva", "email": "joao.silva@email.com", "telefone": "912 345 678"},
            {"nome": "Maria Santos", "email": "maria.santos@email.com", "telefone": "913 456 789"},
            {"nome": "Pedro Oliveira", "email": "pedro.oliveira@email.com", "telefone": "914 567 890"},
            {"nome": "Ana Costa", "email": "ana.costa@email.com", "telefone": "915 678 901"},
            {"nome": "Carlos Ferreira", "email": "carlos.ferreira@email.com", "telefone": "916 789 012"},
            {"nome": "Lúcia Pereira", "email": "lucia.pereira@email.com", "telefone": "917 890 123"},
            {"nome": "Roberto Lima", "email": "roberto.lima@email.com", "telefone": "918 901 234"},
            {"nome": "Fernanda Alves", "email": "fernanda.alves@email.com", "telefone": "919 012 345"}
        ]
        
        clientes = []
        for cliente_data in clientes_data:
            cliente = cliente_service.create_cliente(**cliente_data)
            if cliente:
                clientes.append(cliente)
                print(f"   ✅ {cliente.nome}")
        
        # 5. Criar algumas reservas de exemplo
        print("📅 Criando reservas de exemplo...")
        
        # Reservas para próximos dias (começando amanhã)
        base_date = (datetime.now() + timedelta(days=1)).replace(hour=19, minute=0, second=0, microsecond=0)
        
        reservas_data = [
            {
                "cliente_id": clientes[0].id,
                "mesa_id": mesas[0].id,  # Bella Italiana, Mesa 01
                "data_reserva": base_date,
                "numero_pessoas": 2,
                "observacoes": "Aniversário de casamento"
            },
            {
                "cliente_id": clientes[1].id,
                "mesa_id": mesas[3].id,  # Bella Italiana, Mesa 04
                "data_reserva": base_date + timedelta(hours=1),
                "numero_pessoas": 4,
                "observacoes": "Jantar em família"
            },
            {
                "cliente_id": clientes[2].id,
                "mesa_id": mesas[8].id,  # Sushi Zen, B1
                "data_reserva": base_date + timedelta(days=1),
                "numero_pessoas": 2,
                "observacoes": "Reunião de negócios"
            },
            {
                "cliente_id": clientes[3].id,
                "mesa_id": mesas[13].id,  # Tasca do Porto, P01
                "data_reserva": base_date + timedelta(days=1, hours=1),
                "numero_pessoas": 4,
                "observacoes": "Celebração de promoção"
            },
            {
                "cliente_id": clientes[4].id,
                "mesa_id": mesas[5].id,  # Bella Italiana, E1
                "data_reserva": base_date + timedelta(days=2),
                "numero_pessoas": 4,
                "observacoes": "Jantar romântico"
            },
            {
                "cliente_id": clientes[5].id,
                "mesa_id": mesas[11].id,  # Sushi Zen, V1
                "data_reserva": base_date + timedelta(days=3),
                "numero_pessoas": 8,
                "observacoes": "Reunião de trabalho"
            }
        ]
        
        reservas = []
        for reserva_data in reservas_data:
            reserva = reserva_service.create_reserva(**reserva_data)
            if reserva:
                reservas.append(reserva)
                cliente = next(c for c in clientes if c.id == reserva.cliente_id)
                print(f"   ✅ {cliente.nome} - {reserva.data_reserva.strftime('%d/%m/%Y %H:%M')}")
        
        print(f"\n🎉 Dados de exemplo criados com sucesso!")
        print(f"   📍 {len(restaurantes)} restaurantes")
        print(f"   🏠 {len(ambientes)} ambientes")
        print(f"   🪑 {len(mesas)} mesas")
        print(f"   👥 {len(clientes)} clientes")
        print(f"   📅 {len(reservas)} reservas")
        
        return True
        
    except ValidationError as e:
        print(f"❌ Erro de validação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        logger.error(f"Erro ao criar dados de exemplo: {e}")
        return False


if __name__ == "__main__":
    create_sample_data()