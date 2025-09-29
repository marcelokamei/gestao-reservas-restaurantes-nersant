import streamlit as st
from datetime import datetime, date, timedelta
from typing import List, Optional
from models import Cliente, Mesa, Reserva
from services import cliente_service, restaurante_service, ambiente_service, mesa_service, reserva_service
from utils.validators import ValidationError
from utils.streamlit_utils import StreamlitUtils
from config import Config


class ClientePage:
    """Página do cliente para fazer reservas"""
    
    def __init__(self):
        self.utils = StreamlitUtils()
    
    def render(self):
        """Renderiza a página do cliente"""
        # CSS para página de cliente
        st.markdown("""
        <style>
        /* Ocultar sidebar nativa */
        section[data-testid="stSidebar"] {display: none !important;}
        .css-1d391kg {display: none !important;}
        .stSidebar {display: none !important;}
        
        /* Header do sistema */
        .system-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            margin: -1rem -1rem 2rem -1rem;
            color: white;
            text-align: center;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .system-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .system-header .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-top: 0.5rem;
        }
        
        .client-section {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header principal do sistema
        st.markdown("""
        <div class="system-header">
            <h1>🍽️ Sistema de Gestão de Restaurantes</h1>
            <div class="subtitle">Plataforma completa para gestão de reservas e operações</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Seção específica do cliente
        st.markdown("""
        <div class="client-section">
            <h2>👤 Área do Cliente</h2>
            <p>Bem-vindo! Aqui pode fazer e gerir as suas reservas de mesa.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Verificar se cliente está autenticado
        with st.container():
            if 'cliente_id' not in st.session_state:
                self._render_client_login()
            else:
                # Cliente logado - mostrar tabs
                tab1, tab2 = st.tabs(["🍽️ Fazer Reserva", "👤 Meus Dados"])
                
                with tab1:
                    self._render_reservation_system()
                
                with tab2:
                    self._render_client_profile()
                
                # Botão de logout para clientes logados
                st.markdown("---")
                if st.button("🚪 Terminar Sessão", key="client_logout", type="secondary"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.success("✅ Sessão terminada com sucesso!")
                    st.rerun()
    
    def _render_client_login(self):
        """Renderiza o sistema de login/cadastro do cliente"""
        tab1, tab2 = st.tabs(["Entrar", "Registar"])
        
        with tab1:
            self._render_client_login_form()
        
        with tab2:
            self._render_client_registration_form()
    
    def _render_client_login_form(self):
        """Renderiza formulário de login do cliente"""
        st.subheader("Entre com o seu email")
        
        with st.form("client_login"):
            email = st.text_input("Email", placeholder="seu@email.com")
            submitted = st.form_submit_button("Entrar")
            
            if submitted:
                if email:
                    cliente = cliente_service.get_cliente_by_email(email)
                    if cliente:
                        st.session_state.cliente_id = cliente.id
                        st.session_state.cliente_nome = cliente.nome
                        self.utils.show_success(f"Bem-vindo(a), {cliente.nome}!")
                        st.rerun()
                    else:
                        self.utils.show_error("Cliente não encontrado. Faça o seu registo no separador 'Registar'.")
                else:
                    self.utils.show_error("Por favor, digite o seu email.")
    
    def _render_client_registration_form(self):
        """Renderiza formulário de cadastro do cliente"""
        st.subheader("Registe-se")
        
        with st.form("client_registration"):
            nome = st.text_input("Nome completo", placeholder="O seu nome completo")
            email = st.text_input("Email", placeholder="seu@email.com")
            telefone = st.text_input("Telemóvel", placeholder="912 345 678")
            
            submitted = st.form_submit_button("Registar")
            
            if submitted:
                try:
                    if nome and email and telefone:
                        cliente = cliente_service.create_cliente(nome, email, telefone)
                        if cliente:
                            st.session_state.cliente_id = cliente.id
                            st.session_state.cliente_nome = cliente.nome
                            self.utils.show_success(f"Registo realizado com sucesso! Bem-vindo(a), {cliente.nome}!")
                            st.rerun()
                    else:
                        self.utils.show_error("Por favor, preencha todos os campos.")
                except ValidationError as e:
                    self.utils.show_error(str(e))
                except Exception as e:
                    self.utils.show_error("Erro interno. Tente novamente.")
    
    def _render_reservation_system(self):
        """Renderiza o sistema de reservas"""
        # Header com informações do cliente
        st.write(f"**Cliente:** {st.session_state.cliente_nome}")
        
        st.divider()
        
        # Separadores principais
        tab1, tab2 = st.tabs(["Nova Reserva", "As Minhas Reservas"])
        
        with tab1:
            self._render_new_reservation()
        
        with tab2:
            self._render_my_reservations()
    
    def _render_new_reservation(self):
        """Renderiza formulário de nova reserva"""
        st.subheader("Nova Reserva")
        
        # Passo 1: Selecionar restaurante
        restaurantes = restaurante_service.get_all_restaurantes()
        
        if not restaurantes:
            self.utils.show_warning("Nenhum restaurante disponível de momento.")
            return
        
        restaurante_options = {f"{r.nome} - {r.endereco}": r.id for r in restaurantes}
        restaurante_selected = st.selectbox(
            "Escolha o restaurante:",
            options=list(restaurante_options.keys()),
            key="selected_restaurant"
        )
        
        if restaurante_selected:
            restaurante_id = restaurante_options[restaurante_selected]
            
            # Passo 2: Selecionar ambiente
            ambientes = ambiente_service.get_ambientes_by_restaurante(restaurante_id)
            
            if not ambientes:
                self.utils.show_warning("Este restaurante não possui ambientes cadastrados.")
                return
            
            ambiente_options = {f"{a.nome}": a.id for a in ambientes}
            ambiente_selected = st.selectbox(
                "Escolha o ambiente:",
                options=list(ambiente_options.keys()),
                key="selected_environment"
            )
            
            if ambiente_selected:
                ambiente_id = ambiente_options[ambiente_selected]
                
                # Passo 3: Selecionar data e horário
                col1, col2 = st.columns(2)
                
                with col1:
                    data_reserva = st.date_input(
                        "Data da reserva:",
                        min_value=date.today(),
                        max_value=date.today() + timedelta(days=90),
                        key="reservation_date"
                    )
                
                with col2:
                    horario = st.selectbox(
                        "Horário:",
                        options=Config.TIME_SLOTS,
                        key="reservation_time"
                    )
                
                # Passo 4: Número de pessoas
                numero_pessoas = st.number_input(
                    "Número de pessoas:",
                    min_value=1,
                    max_value=20,
                    value=2,
                    key="number_people"
                )
                
                # Passo 5: Buscar mesas disponíveis
                if st.button("Buscar Mesas Disponíveis", type="primary"):
                    data_hora_reserva = datetime.combine(data_reserva, datetime.strptime(horario, "%H:%M").time())
                    
                    mesas_disponiveis = mesa_service.get_available_tables(
                        ambiente_id, data_hora_reserva, numero_pessoas
                    )
                    
                    if mesas_disponiveis:
                        st.session_state.mesas_disponiveis = mesas_disponiveis
                        st.session_state.data_hora_reserva = data_hora_reserva
                        self.utils.show_success(f"Encontradas {len(mesas_disponiveis)} mesa(s) disponível(is)!")
                    else:
                        self.utils.show_warning("Nenhuma mesa disponível para os critérios selecionados.")
                
                # Passo 6: Selecionar mesa e confirmar reserva
                if 'mesas_disponiveis' in st.session_state and st.session_state.mesas_disponiveis:
                    st.subheader("Mesas Disponíveis")
                    
                    # Exibir mesas em cards
                    cols = st.columns(min(len(st.session_state.mesas_disponiveis), 3))
                    
                    for i, mesa in enumerate(st.session_state.mesas_disponiveis):
                        col_index = i % 3
                        with cols[col_index]:
                            with st.container():
                                st.markdown(f"""
                                <div class="table-card">
                                    <h4>Mesa {mesa.numero}</h4>
                                    <p>Capacidade: {mesa.capacidade} pessoas</p>
                                    {f'<p><small>{mesa.observacoes}</small></p>' if mesa.observacoes else ''}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button(f"Seleccionar Mesa {mesa.numero}", key=f"select_table_{mesa.id}"):
                                    st.session_state.mesa_selecionada = mesa.id
                                    st.session_state.numero_pessoas_reserva = numero_pessoas
                                    st.rerun()
                
                # Passo 7: Confirmar reserva da mesa selecionada
                if 'mesa_selecionada' in st.session_state:
                    self._render_reservation_confirmation()
    
    def _render_reservation_confirmation(self):
        """Renderiza o formulário de confirmação da reserva"""
        # Verificar se temos todos os dados necessários
        if 'mesa_selecionada' not in st.session_state or 'numero_pessoas_reserva' not in st.session_state:
            st.error("❌ Dados da reserva perdidos. Tente novamente.")
            return
        
        if 'data_hora_reserva' not in st.session_state or 'cliente_id' not in st.session_state:
            st.error("❌ Dados da sessão perdidos. Faça login novamente.")
            return
        
        mesa_id = st.session_state.mesa_selecionada
        numero_pessoas = st.session_state.numero_pessoas_reserva
        
        # Obter informações da mesa selecionada com verificação de erros
        try:
            mesa = mesa_service.get_mesa_by_id(mesa_id)
            if not mesa:
                st.error("❌ Mesa não encontrada.")
                return
                
            ambiente = ambiente_service.get_ambiente_by_id(mesa.ambiente_id)
            if not ambiente:
                st.error("❌ Ambiente não encontrado.")
                return
                
            restaurante = restaurante_service.get_restaurante_by_id(ambiente.restaurante_id)
            if not restaurante:
                st.error("❌ Restaurante não encontrado.")
                return
        except Exception as e:
            st.error(f"❌ Erro ao obter dados: {str(e)}")
            return
        
        st.subheader("🍽️ Confirmar Reserva")
        
        # Mostrar resumo da reserva
        with st.container():
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                <h4>📋 Resumo da Reserva</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Restaurante:** {restaurante.nome}")
                st.write(f"**Ambiente:** {ambiente.nome}")
                st.write(f"**Mesa:** {mesa.numero}")
            with col2:
                st.write(f"**Data/Hora:** {st.session_state.data_hora_reserva.strftime('%d/%m/%Y às %H:%M')}")
                st.write(f"**Pessoas:** {numero_pessoas}")
                st.write(f"**Capacidade da Mesa:** {mesa.capacidade}")
        
        # Botão de cancelar (fora do formulário)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("❌ Cancelar", type="secondary", key="cancel_reservation"):
                # Limpar seleção
                if 'mesa_selecionada' in st.session_state:
                    del st.session_state.mesa_selecionada
                if 'numero_pessoas_reserva' in st.session_state:
                    del st.session_state.numero_pessoas_reserva
                st.rerun()
        
        # Formulário de confirmação simplificado
        st.markdown("### 📝 Confirmar Reserva")
        
        observacoes = st.text_area(
            "Observações (opcional):", 
            placeholder="Alguma observação especial para a sua reserva?",
            help="Por exemplo: aniversário, preferências alimentares, etc.",
            key="obs_reserva"
        )
        
        # Usar botão simples em vez de formulário
        if st.button("✅ Confirmar Reserva", type="primary", key="btn_confirmar"):
            with st.spinner("Criando reserva..."):
                try:
                    # Log para debug
                    st.write(f"🔄 Criando reserva para cliente {st.session_state.cliente_id}")
                    
                    reserva = reserva_service.create_reserva(
                        cliente_id=st.session_state.cliente_id,
                        mesa_id=mesa_id,
                        data_reserva=st.session_state.data_hora_reserva,
                        numero_pessoas=numero_pessoas,
                        observacoes=observacoes.strip() if observacoes and observacoes.strip() else None
                    )
                    
                    if reserva:
                        st.success("🎉 Reserva criada com sucesso!")
                        st.balloons()
                        
                        # Mostrar detalhes imediatamente
                        with st.expander("📄 Detalhes da Reserva", expanded=True):
                            st.write(f"**ID da Reserva:** {reserva.id}")
                            st.write(f"**Restaurante:** {restaurante.nome}")
                            st.write(f"**Ambiente:** {ambiente.nome}")
                            st.write(f"**Mesa:** {mesa.numero}")
                            st.write(f"**Data/Hora:** {reserva.data_reserva.strftime('%d/%m/%Y às %H:%M')}")
                            st.write(f"**Pessoas:** {reserva.numero_pessoas}")
                            st.write(f"**Status:** {reserva.status.title()}")
                            if reserva.observacoes:
                                st.write(f"**Observações:** {reserva.observacoes}")
                        
                        # Limpar dados da sessão após mostrar sucesso
                        keys_to_clear = [
                            'mesas_disponiveis', 'data_hora_reserva', 
                            'mesa_selecionada', 'numero_pessoas_reserva'
                        ]
                        for key in keys_to_clear:
                            if key in st.session_state:
                                del st.session_state[key]
                        
                        st.info("💡 Pode gerir as suas reservas na aba 'Minhas Reservas'")
                        
                        # Forçar atualização após um delay
                        import time
                        time.sleep(2)
                        st.rerun()
                        
                    else:
                        st.error("❌ Erro ao criar reserva. Tente novamente.")
                        
                except ValidationError as e:
                    st.error(f"❌ Erro de validação: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Erro interno: {str(e)}")
                    st.exception(e)

    
    def _render_my_reservations(self):
        """Renderiza as reservas do cliente"""
        st.subheader("Minhas Reservas")
        
        reservas = reserva_service.get_reservas_by_cliente(st.session_state.cliente_id)
        
        if not reservas:
            self.utils.show_info("Você ainda não possui reservas.")
            return
        
        # Filtrar por status
        status_filter = st.selectbox(
            "Filtrar por status:",
            options=["Todas", "Confirmadas", "Canceladas"],
            key="reservation_filter"
        )
        
        # Aplicar filtro
        if status_filter == "Confirmadas":
            reservas = [r for r in reservas if r.status == 'confirmada']
        elif status_filter == "Canceladas":
            reservas = [r for r in reservas if r.status == 'cancelada']
        
        # Exibir reservas
        for reserva in reservas:
            mesa = mesa_service.get_mesa_by_id(reserva.mesa_id)
            ambiente = ambiente_service.get_ambiente_by_id(mesa.ambiente_id)
            restaurante = restaurante_service.get_restaurante_by_id(ambiente.restaurante_id)
            
            # Card da reserva
            with st.expander(
                f"📅 {reserva.data_reserva.strftime('%d/%m/%Y %H:%M')} - {restaurante.nome} - Mesa {mesa.numero}",
                expanded=False
            ):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Restaurante:** {restaurante.nome}")
                    st.write(f"**Endereço:** {restaurante.endereco}")
                    st.write(f"**Ambiente:** {ambiente.nome}")
                    st.write(f"**Mesa:** {mesa.numero} (Capacidade: {mesa.capacidade})")
                    st.write(f"**Pessoas:** {reserva.numero_pessoas}")
                    st.write(f"**Status:** {reserva.status.upper()}")
                    if reserva.observacoes:
                        st.write(f"**Observações:** {reserva.observacoes}")
                
                with col2:
                    # Permitir cancelamento apenas para reservas confirmadas e futuras
                    if (reserva.status == 'confirmada' and 
                        reserva.data_reserva > datetime.now()):
                        
                        if self.utils.create_confirmation_dialog(
                            "Cancelar Reserva",
                            "Tem certeza que deseja cancelar esta reserva?",
                            f"cancel_{reserva.id}"
                        ):
                            if reserva_service.cancel_reserva(reserva.id):
                                self.utils.show_success("Reserva cancelada com sucesso!")
                                st.rerun()
                            else:
                                self.utils.show_error("Erro ao cancelar reserva.")

    def _render_client_profile(self):
        """Renderiza a seção de perfil do cliente para atualização de dados"""
        st.markdown("### 👤 Meus Dados")
        
        # Buscar dados atuais do cliente
        cliente_id = st.session_state.get('cliente_id')
        cliente = cliente_service.get_cliente_by_id(cliente_id)
        
        if not cliente:
            st.error("❌ Erro ao carregar dados do cliente.")
            return
        
        st.info("💡 Atualize os seus dados pessoais abaixo:")
        
        with st.form("update_client_profile"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("👤 Nome:", value=cliente.nome)
                email = st.text_input("📧 Email:", value=cliente.email)
            
            with col2:
                telefone = st.text_input("📱 Telefone:", value=cliente.telefone)
                st.write("")  # Espaçamento
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button("✅ Atualizar Dados", type="primary")
        
        if submitted:
            if nome and email and telefone:
                try:
                    # Atualizar dados do cliente
                    updated_cliente = cliente_service.update_cliente_dados(
                        cliente_id, nome, email, telefone
                    )
                    
                    if updated_cliente:
                        # Atualizar dados na sessão
                        st.session_state.cliente_nome = updated_cliente.nome
                        st.session_state.logged_user_data.update({
                            "nome": updated_cliente.nome,
                            "email": updated_cliente.email,
                            "telefone": updated_cliente.telefone
                        })
                        
                        st.success("✅ Dados atualizados com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao atualizar dados.")
                except Exception as e:
                    if "UNIQUE constraint failed" in str(e):
                        st.error("❌ Email já está sendo utilizado por outro cliente.")
                    else:
                        st.error(f"❌ Erro: {str(e)}")
            else:
                st.error("❌ Por favor, preencha todos os campos.")
        
        # Mostrar histórico de reservas
        st.markdown("---")
        st.markdown("### 📋 Histórico de Reservas")
        
        reservas = reserva_service.get_reservas_by_cliente(cliente_id)
        
        if reservas:
            for reserva in reservas:
                try:
                    # Buscar dados relacionados
                    mesa = mesa_service.get_mesa_by_id(reserva.mesa_id)
                    ambiente = ambiente_service.get_ambiente_by_id(mesa.ambiente_id)
                    restaurante = restaurante_service.get_restaurante_by_id(ambiente.restaurante_id)
                    
                    with st.expander(f"🍽️ {restaurante.nome} - {reserva.data_reserva.strftime('%d/%m/%Y %H:%M')}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Mesa:** {mesa.numero}")
                            st.write(f"**Ambiente:** {ambiente.nome}")
                        
                        with col2:
                            st.write(f"**Pessoas:** {reserva.numero_pessoas}")
                            status_color = "🟢" if reserva.status == "confirmada" else "🔴" if reserva.status == "cancelada" else "🟡"
                            st.write(f"**Status:** {status_color} {reserva.status.title()}")
                        
                        with col3:
                            if reserva.observacoes:
                                st.write(f"**Observações:** {reserva.observacoes}")
                except Exception as e:
                    st.error(f"Erro ao carregar dados da reserva: {e}")
        else:
            st.info("📝 Ainda não fez nenhuma reserva.")


def render_client_page():
    """Função principal para renderizar a página do cliente"""
    page = ClientePage()
    page.render()