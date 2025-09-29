import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from models import Restaurante, Ambiente, Mesa, Reserva, Cliente
from services import (
    restaurante_service, ambiente_service, mesa_service, 
    reserva_service, cliente_service
)
from utils.validators import ValidationError
from utils.streamlit_utils import StreamlitUtils
from config import Config


class AdminPage:
    """Página administrativa do sistema"""
    
    def __init__(self):
        self.utils = StreamlitUtils()
    
    def render(self):
        """Renderiza a página do administrador com sidebar personalizada"""
        # CSS para página admin
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
        
        .admin-sidebar {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .admin-sidebar h3 {
            color: white;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .admin-info {
            background-color: #e3f2fd;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            text-align: center;
            border-left: 4px solid #2196f3;
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
        
        # Layout principal com colunas
        col_sidebar, col_main = st.columns([1, 4])
        
        with col_sidebar:
            self._render_custom_sidebar()
        
        with col_main:
            self._render_main_content()
    
    def _render_custom_sidebar(self):
        """Renderiza nossa sidebar personalizada"""
        with st.container():
            st.markdown('<div class="admin-sidebar">', unsafe_allow_html=True)
            st.markdown("### 🍽️ Admin Panel")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Opções do menu
        menu_options = [
            ("📊", "Dashboard"),
            ("🏢", "Restaurantes"),
            ("🌿", "Ambientes"),
            ("🪑", "Mesas"),
            ("📅", "Reservas"),
            ("👤", "Clientes"),
            ("👥", "Utilizadores"),
            ("📈", "Relatórios")
        ]
        
        # Estado do menu (usar session_state para persistir)
        if "selected_menu" not in st.session_state:
            st.session_state.selected_menu = "Dashboard"
        
        current_selection = st.session_state.selected_menu
        
        # Renderizar opções do menu
        for icon, option in menu_options:
            button_type = "primary" if option == current_selection else "secondary"
            if st.button(f"{icon} {option}", key=f"menu_{option}", type=button_type):
                st.session_state.selected_menu = option
                st.rerun()
        
        # Informações do admin
        with st.container():
            st.markdown('<div class="admin-info">', unsafe_allow_html=True)
            st.write("👨‍💼 **Administrador**")
            st.write("✅ Status: Online")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Botão de logout
        if st.button("🚪 Terminar Sessão", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    def _render_main_content(self):
        """Renderiza o conteúdo principal baseado na seleção do menu"""
        selected = st.session_state.get("selected_menu", "Dashboard")
        
        st.title(f"⚙️ {selected}")
        self._render_content(selected)
    
    def _render_content(self, menu):
        """Renderiza o conteúdo principal baseado no menu selecionado"""
        if menu == "Dashboard":
            self._render_dashboard()
        elif menu == "Restaurantes":
            self._render_restaurants()
        elif menu == "Ambientes":
            self._render_environments()
        elif menu == "Mesas":
            self._render_tables()
        elif menu == "Reservas":
            self._render_reservations()
        elif menu == "Clientes":
            self._render_clients()
        elif menu == "Utilizadores":
            self._render_users()
        elif menu == "Relatórios":
            self._render_reports()
        else:
            st.info(f"Seção {menu} em desenvolvimento")
    
    def _render_dashboard(self):
        """Renderiza o dashboard principal"""
        st.subheader("📊 Dashboard")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_restaurants = len(restaurante_service.get_all_restaurantes())
            st.metric("🏢 Restaurantes", str(total_restaurants))
        
        with col2:
            total_clients = len(cliente_service.get_all_clientes())
            st.metric("👤 Clientes", str(total_clients))
        
        with col3:
            # Reservas hoje
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            reservas_hoje = reserva_service.get_reservas_by_data(today)
            active_reservas = [r for r in reservas_hoje if r.status == 'confirmada']
            st.metric("📅 Reservas Hoje", str(len(active_reservas)))
        
        with col4:
            # Total de mesas
            total_tables = 0
            for restaurant in restaurante_service.get_all_restaurantes():
                for ambiente in ambiente_service.get_ambientes_by_restaurante(restaurant.id):
                    total_tables += len(mesa_service.get_mesas_by_ambiente(ambiente.id))
            st.metric("🪑 Total de Mesas", str(total_tables))
        
        st.divider()
        
        # Reservas próximas
        st.subheader("📅 Próximas Reservas")
        
        # Buscar reservas dos próximos 7 dias (incluindo hoje)
        start_date = date.today()
        end_date = start_date + timedelta(days=7)
        
        reservas_recentes = []
        for i in range(8):  # Hoje + próximos 7 dias
            current_date = start_date + timedelta(days=i)
            # Converter date para datetime
            current_datetime = datetime.combine(current_date, datetime.min.time())
            daily_reservas = reserva_service.get_reservas_by_data(current_datetime)
            reservas_recentes.extend(daily_reservas)
        
        if reservas_recentes:
            # Preparar dados para tabela
            reservas_data = []
            for reserva in reservas_recentes[-10:]:  # Últimas 10 reservas
                try:
                    cliente = cliente_service.get_cliente_by_id(reserva.cliente_id)
                    mesa = mesa_service.get_mesa_by_id(reserva.mesa_id)
                    ambiente = ambiente_service.get_ambiente_by_id(mesa.ambiente_id)
                    restaurante = restaurante_service.get_restaurante_by_id(ambiente.restaurante_id)
                    
                    reservas_data.append({
                        "Data/Hora": reserva.data_reserva.strftime("%d/%m/%Y %H:%M"),
                        "Cliente": cliente.nome,
                        "Restaurante": restaurante.nome,
                        "Mesa": mesa.numero,
                        "Pessoas": reserva.numero_pessoas,
                        "Status": reserva.status.capitalize()
                    })
                except:
                    continue
            
            if reservas_data:
                df = pd.DataFrame(reservas_data)
                st.dataframe(df, width='stretch')
            else:
                self.utils.show_info("Nenhuma reserva encontrada.")
        else:
            self.utils.show_info("Nenhuma reserva nos próximos 7 dias.")
    
    def _render_restaurants(self):
        """Renderiza gerenciamento de restaurantes"""
        st.subheader("🏪 Gerenciamento de Restaurantes")
        
        tab1, tab2 = st.tabs(["Lista de Restaurantes", "Novo Restaurante"])
        
        with tab1:
            self._render_restaurants_list()
        
        with tab2:
            self._render_new_restaurant_form()
    
    def _render_restaurants_list(self):
        """Renderiza lista de restaurantes"""
        restaurants = restaurante_service.get_all_restaurantes()
        
        if not restaurants:
            self.utils.show_info("Nenhum restaurante cadastrado.")
            return
        
        for restaurant in restaurants:
            with st.expander(f"🏪 {restaurant.nome}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Morada:** {restaurant.endereco}")
                    st.write(f"**Telemóvel:** {restaurant.telefone}")
                    if restaurant.email:
                        st.write(f"**Email:** {restaurant.email}")
                    if restaurant.descricao:
                        st.write(f"**Descrição:** {restaurant.descricao}")
                    
                    # Estatísticas do restaurante
                    ambientes = ambiente_service.get_ambientes_by_restaurante(restaurant.id)
                    total_mesas = sum(len(mesa_service.get_mesas_by_ambiente(amb.id)) for amb in ambientes)
                    reservas = reserva_service.get_reservas_by_restaurante(restaurant.id)
                    
                    st.write(f"**Ambientes:** {len(ambientes)}")
                    st.write(f"**Mesas:** {total_mesas}")
                    st.write(f"**Reservas:** {len(reservas)}")
                
                with col2:
                    if st.button(f"Editar", key=f"edit_restaurant_{restaurant.id}"):
                        st.session_state[f"editing_restaurant_{restaurant.id}"] = True
                    
                    if self.utils.create_confirmation_dialog(
                        "Excluir",
                        f"Tem certeza que deseja excluir o restaurante {restaurant.nome}?",
                        f"delete_restaurant_{restaurant.id}"
                    ):
                        if restaurante_service.delete_restaurante(restaurant.id):
                            self.utils.show_success("Restaurante excluído com sucesso!")
                            st.rerun()
                        else:
                            self.utils.show_error("Erro ao excluir restaurante.")
                
                # Formulário de edição
                if st.session_state.get(f"editing_restaurant_{restaurant.id}", False):
                    self._render_edit_restaurant_form(restaurant)
    
    def _render_new_restaurant_form(self):
        """Renderiza formulário de novo restaurante"""
        with st.form("new_restaurant"):
            st.write("**Dados do Restaurante**")
            
            nome = st.text_input("Nome*", placeholder="Nome do restaurante")
            endereco = st.text_area("Morada*", placeholder="Morada completa")
            telefone = st.text_input("Telemóvel*", placeholder="213 456 789")
            email = st.text_input("Email", placeholder="contato@restaurante.com")
            descricao = st.text_area("Descrição", placeholder="Descrição do restaurante")
            
            submitted = st.form_submit_button("Registar Restaurante", type="primary")
            
            if submitted:
                try:
                    if nome and endereco and telefone:
                        restaurant = restaurante_service.create_restaurante(
                            nome=nome,
                            endereco=endereco,
                            telefone=telefone,
                            email=email if email else None,
                            descricao=descricao if descricao else None
                        )
                        
                        if restaurant:
                            self.utils.show_success(f"Restaurante '{restaurant.nome}' registado com sucesso!")
                            st.rerun()
                    else:
                        self.utils.show_error("Por favor, preencha todos os campos obrigatórios (*).")
                        
                except ValidationError as e:
                    self.utils.show_error(str(e))
                except Exception as e:
                    self.utils.show_error("Erro interno. Tente novamente.")
    
    def _render_edit_restaurant_form(self, restaurant: Restaurante):
        """Renderiza formulário de edição de restaurante"""
        with st.form(f"edit_restaurant_{restaurant.id}"):
            st.write("**Editar Restaurante**")
            
            nome = st.text_input("Nome*", value=restaurant.nome)
            endereco = st.text_area("Morada*", value=restaurant.endereco)
            telefone = st.text_input("Telemóvel*", value=restaurant.telefone)
            email = st.text_input("Email", value=restaurant.email or "")
            descricao = st.text_area("Descrição", value=restaurant.descricao or "")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Salvar Alterações", type="primary")
            with col2:
                canceled = st.form_submit_button("Cancelar")
            
            if submitted:
                try:
                    updated_restaurant = restaurante_service.update_restaurante(
                        restaurant.id,
                        nome=nome,
                        endereco=endereco,
                        telefone=telefone,
                        email=email if email else None,
                        descricao=descricao if descricao else None
                    )
                    
                    if updated_restaurant:
                        self.utils.show_success("Restaurante atualizado com sucesso!")
                        del st.session_state[f"editing_restaurant_{restaurant.id}"]
                        st.rerun()
                        
                except ValidationError as e:
                    self.utils.show_error(str(e))
                except Exception as e:
                    self.utils.show_error("Erro interno. Tente novamente.")
            
            if canceled:
                del st.session_state[f"editing_restaurant_{restaurant.id}"]
                st.rerun()
    
    def _render_environments(self):
        """Renderiza gerenciamento de ambientes"""
        st.subheader("🏠 Gerenciamento de Ambientes")
        
        # Seletor de restaurante
        restaurants = restaurante_service.get_all_restaurantes()
        
        if not restaurants:
            self.utils.show_warning("Cadastre pelo menos um restaurante antes de criar ambientes.")
            return
        
        restaurant_options = {r.nome: r.id for r in restaurants}
        selected_restaurant = st.selectbox(
            "Selecione um restaurante:",
            options=list(restaurant_options.keys()),
            key="env_restaurant_selector"
        )
        
        if selected_restaurant:
            restaurant_id = restaurant_options[selected_restaurant]
            
            tab1, tab2 = st.tabs(["Ambientes", "Novo Ambiente"])
            
            with tab1:
                self._render_environments_list(restaurant_id)
            
            with tab2:
                self._render_new_environment_form(restaurant_id)
    
    def _render_environments_list(self, restaurant_id: int):
        """Renderiza lista de ambientes"""
        environments = ambiente_service.get_ambientes_by_restaurante(restaurant_id)
        
        if not environments:
            self.utils.show_info("Nenhum ambiente cadastrado para este restaurante.")
            return
        
        for environment in environments:
            with st.expander(f"🏠 {environment.nome}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if environment.descricao:
                        st.write(f"**Descrição:** {environment.descricao}")
                    
                    # Estatísticas do ambiente
                    mesas = mesa_service.get_mesas_by_ambiente(environment.id)
                    st.write(f"**Mesas:** {len(mesas)}")
                    
                    if mesas:
                        capacidade_total = sum(mesa.capacidade for mesa in mesas)
                        st.write(f"**Capacidade Total:** {capacidade_total} pessoas")
                
                with col2:
                    if st.button(f"Editar", key=f"edit_env_{environment.id}"):
                        st.session_state[f"editing_env_{environment.id}"] = True
                    
                    if self.utils.create_confirmation_dialog(
                        "Excluir",
                        f"Tem certeza que deseja excluir o ambiente {environment.nome}?",
                        f"delete_env_{environment.id}"
                    ):
                        if ambiente_service.delete_ambiente(environment.id):
                            self.utils.show_success("Ambiente excluído com sucesso!")
                            st.rerun()
                        else:
                            self.utils.show_error("Erro ao excluir ambiente.")
                
                # Formulário de edição
                if st.session_state.get(f"editing_env_{environment.id}", False):
                    self._render_edit_environment_form(environment)
    
    def _render_new_environment_form(self, restaurant_id: int):
        """Renderiza formulário de novo ambiente"""
        with st.form("new_environment"):
            st.write("**Dados do Ambiente**")
            
            nome = st.text_input("Nome*", placeholder="Ex: Salão Principal, Terraço, etc.")
            descricao = st.text_area("Descrição", placeholder="Descrição do ambiente")
            
            submitted = st.form_submit_button("Cadastrar Ambiente", type="primary")
            
            if submitted:
                try:
                    if nome:
                        environment = ambiente_service.create_ambiente(
                            nome=nome,
                            restaurante_id=restaurant_id,
                            descricao=descricao if descricao else None
                        )
                        
                        if environment:
                            self.utils.show_success(f"Ambiente '{environment.nome}' cadastrado com sucesso!")
                            st.rerun()
                    else:
                        self.utils.show_error("Por favor, preencha o nome do ambiente.")
                        
                except ValidationError as e:
                    self.utils.show_error(str(e))
                except Exception as e:
                    self.utils.show_error("Erro interno. Tente novamente.")
    
    def _render_edit_environment_form(self, environment: Ambiente):
        """Renderiza formulário de edição de ambiente"""
        with st.form(f"edit_environment_{environment.id}"):
            st.write("**Editar Ambiente**")
            
            nome = st.text_input("Nome*", value=environment.nome)
            descricao = st.text_area("Descrição", value=environment.descricao or "")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Salvar Alterações", type="primary")
            with col2:
                canceled = st.form_submit_button("Cancelar")
            
            if submitted:
                try:
                    updated_environment = ambiente_service.update_ambiente(
                        environment.id,
                        nome=nome,
                        descricao=descricao if descricao else None
                    )
                    
                    if updated_environment:
                        self.utils.show_success("Ambiente atualizado com sucesso!")
                        del st.session_state[f"editing_env_{environment.id}"]
                        st.rerun()
                        
                except ValidationError as e:
                    self.utils.show_error(str(e))
                except Exception as e:
                    self.utils.show_error("Erro interno. Tente novamente.")
            
            if canceled:
                del st.session_state[f"editing_env_{environment.id}"]
                st.rerun()
    
    def _render_tables(self):
        """Renderiza gerenciamento de mesas"""
        st.subheader("🪑 Gerenciamento de Mesas")
        
        # Seleção hierárquica: Restaurante -> Ambiente
        restaurants = restaurante_service.get_all_restaurantes()
        
        if not restaurants:
            self.utils.show_warning("Cadastre pelo menos um restaurante antes de criar mesas.")
            return
        
        restaurant_options = {r.nome: r.id for r in restaurants}
        selected_restaurant = st.selectbox(
            "Selecione um restaurante:",
            options=list(restaurant_options.keys()),
            key="table_restaurant_selector"
        )
        
        if selected_restaurant:
            restaurant_id = restaurant_options[selected_restaurant]
            environments = ambiente_service.get_ambientes_by_restaurante(restaurant_id)
            
            if not environments:
                self.utils.show_warning("Cadastre pelo menos um ambiente antes de criar mesas.")
                return
            
            environment_options = {e.nome: e.id for e in environments}
            selected_environment = st.selectbox(
                "Selecione um ambiente:",
                options=list(environment_options.keys()),
                key="table_environment_selector"
            )
            
            if selected_environment:
                environment_id = environment_options[selected_environment]
                
                tab1, tab2 = st.tabs(["Mesas", "Nova Mesa"])
                
                with tab1:
                    self._render_tables_list(environment_id)
                
                with tab2:
                    self._render_new_table_form(environment_id)
    
    def _render_tables_list(self, environment_id: int):
        """Renderiza lista de mesas"""
        try:
            tables = mesa_service.get_mesas_by_ambiente(environment_id)
            
            if not tables:
                self.utils.show_info("Nenhuma mesa cadastrada para este ambiente.")
                return
            
            # Mostrar informações básicas
            st.info(f"� {len(tables)} mesa(s) encontrada(s) neste ambiente")
            
            # Renderizar usando dataframe para garantir visualização
            st.subheader("Lista de Mesas")
            
            # Preparar dados para tabela
            table_data = []
            for table in tables:
                table_data.append({
                    "Mesa": table.numero,
                    "Capacidade": f"{table.capacidade} pessoas",
                    "Observações": table.observacoes or "-",
                    "ID": table.id
                })
            
            if table_data:
                import pandas as pd
                df = pd.DataFrame(table_data)
                st.dataframe(df, width='stretch', hide_index=True)
            
            st.divider()
            
            # Grid visual de mesas (versão mais robusta)
            st.subheader("Gestão de Mesas")
            
            # Usar layout mais simples e confiável
            for i, table in enumerate(tables):
                with st.expander(f"🪑 Mesa {table.numero} - {table.capacidade} pessoas"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Mesa:** {table.numero}")
                        st.write(f"**Capacidade:** {table.capacidade} pessoas")
                        if table.observacoes:
                            st.write(f"**Observações:** {table.observacoes}")
                    
                    with col2:
                        if st.button("✏️ Editar", key=f"edit_table_{table.id}"):
                            st.session_state[f"editing_table_{table.id}"] = True
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️ Excluir", key=f"delete_table_{table.id}"):
                            if st.session_state.get(f"confirm_delete_{table.id}", False):
                                if mesa_service.delete_mesa(table.id):
                                    self.utils.show_success("Mesa excluída com sucesso!")
                                    st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{table.id}"] = True
                                st.warning("Clique novamente para confirmar exclusão")
                                st.rerun()
                    
                    # Formulário de edição
                    if st.session_state.get(f"editing_table_{table.id}", False):
                        st.divider()
                        self._render_edit_table_form(table)
                        
        except Exception as e:
            st.error(f"❌ Erro na renderização de mesas: {str(e)}")
            st.error("Por favor, tente atualizar a página ou contacte o suporte técnico.")
    
    def _render_new_table_form(self, environment_id: int):
        """Renderiza formulário de nova mesa"""
        with st.form("new_table"):
            st.write("**Dados da Mesa**")
            
            numero = st.text_input("Número da Mesa*", placeholder="Ex: 01, A1, etc.")
            capacidade = st.number_input("Capacidade*", min_value=1, max_value=20, value=4)
            observacoes = st.text_area("Observações", placeholder="Ex: Mesa próxima à janela")
            
            submitted = st.form_submit_button("Cadastrar Mesa", type="primary")
            
            if submitted:
                try:
                    if numero:
                        table = mesa_service.create_mesa(
                            numero=numero,
                            capacidade=capacidade,
                            ambiente_id=environment_id,
                            observacoes=observacoes if observacoes else None
                        )
                        
                        if table:
                            self.utils.show_success(f"Mesa '{table.numero}' cadastrada com sucesso!")
                            st.rerun()
                    else:
                        self.utils.show_error("Por favor, preencha o número da mesa.")
                        
                except ValidationError as e:
                    self.utils.show_error(str(e))
                except Exception as e:
                    import traceback
                    error_msg = f"Erro interno: {str(e)}"
                    st.error(error_msg)
                    # Debug: mostrar traceback no log
                    print(f"Error in _render_new_table_form: {traceback.format_exc()}")
    
    def _render_edit_table_form(self, table: Mesa):
        """Renderiza formulário de edição de mesa"""
        with st.form(f"edit_table_{table.id}"):
            st.write("**Editar Mesa**")
            
            numero = st.text_input("Número da Mesa*", value=table.numero)
            capacidade = st.number_input("Capacidade*", min_value=1, max_value=20, value=table.capacidade)
            observacoes = st.text_area("Observações", value=table.observacoes or "")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Salvar Alterações", type="primary")
            with col2:
                canceled = st.form_submit_button("Cancelar")
            
            if submitted:
                try:
                    updated_table = mesa_service.update_mesa(
                        table.id,
                        numero=numero,
                        capacidade=capacidade,
                        observacoes=observacoes if observacoes else None
                    )
                    
                    if updated_table:
                        self.utils.show_success("Mesa atualizada com sucesso!")
                        del st.session_state[f"editing_table_{table.id}"]
                        st.rerun()
                        
                except ValidationError as e:
                    self.utils.show_error(str(e))
                except Exception as e:
                    self.utils.show_error("Erro interno. Tente novamente.")
            
            if canceled:
                del st.session_state[f"editing_table_{table.id}"]
                st.rerun()
    
    def _render_reservations(self):
        """Renderiza gerenciamento de reservas"""
        st.subheader("📅 Gerenciamento de Reservas")
        
        # Filtros
        st.write("**Filtros de Pesquisa**")
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "📅 Data Inicial:",
                value=date.today() - timedelta(days=7),  # Última semana por padrão
                key="reservation_start_date_filter"
            )
        
        with col2:
            end_date = st.date_input(
                "📅 Data Final:",
                value=date.today(),
                key="reservation_end_date_filter"
            )
        
        # Validação das datas
        if start_date > end_date:
            st.error("❌ A data inicial deve ser anterior à data final.")
            return
        
        # Mostrar período selecionado
        days_diff = (end_date - start_date).days + 1
        st.info(f"📊 Período selecionado: {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')} ({days_diff} dias)")
        
        col3, col4 = st.columns(2)
        
        with col3:
            status_options = ["Todas", "Confirmadas", "Canceladas"]
            status_filter = st.selectbox(
                "Status:",
                options=status_options,
                key="reservation_status_filter"
            )
        
        with col4:
            restaurants = restaurante_service.get_all_restaurantes()
            restaurant_options = ["Todos"] + [r.nome for r in restaurants]
            restaurant_filter = st.selectbox(
                "Restaurante:",
                options=restaurant_options,
                key="reservation_restaurant_filter"
            )
        
        # Buscar reservas no período selecionado
        reservations = []
        current_date = start_date
        
        with st.spinner(f"🔍 Buscando reservas de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}..."):
            while current_date <= end_date:
                current_datetime = datetime.combine(current_date, datetime.min.time())
                daily_reservations = reserva_service.get_reservas_by_data(current_datetime)
                reservations.extend(daily_reservations)
                current_date += timedelta(days=1)
        
        # Aplicar filtros
        if status_filter != "Todas":
            status_value = status_filter.lower().rstrip('s')  # "confirmadas" -> "confirmada"
            reservations = [r for r in reservations if r.status == status_value]
        
        if restaurant_filter != "Todos":
            restaurant_id = next(r.id for r in restaurants if r.nome == restaurant_filter)
            restaurant_reservations = reserva_service.get_reservas_by_restaurante(restaurant_id)
            reservation_ids = [r.id for r in restaurant_reservations]
            reservations = [r for r in reservations if r.id in reservation_ids]
        
        # Exibir reservas
        if not reservations:
            self.utils.show_info("Nenhuma reserva encontrada para os filtros selecionados.")
            return
        
        # Estatísticas do período
        confirmadas = [r for r in reservations if r.status == 'confirmada']
        canceladas = [r for r in reservations if r.status == 'cancelada']
        total_pessoas = sum(r.numero_pessoas for r in confirmadas)
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Reservas", len(reservations))
        with col2:
            st.metric("Confirmadas", len(confirmadas))
        with col3:
            st.metric("Canceladas", len(canceladas))
        with col4:
            st.metric("Total Pessoas", total_pessoas)
        
        st.divider()
        
        # Tabela resumo
        st.subheader("📋 Tabela Resumo")
        
        # Preparar dados para tabela
        table_data = []
        for reservation in reservations:
            try:
                cliente = cliente_service.get_cliente_by_id(reservation.cliente_id)
                mesa = mesa_service.get_mesa_by_id(reservation.mesa_id)
                ambiente = ambiente_service.get_ambiente_by_id(mesa.ambiente_id)
                restaurante = restaurante_service.get_restaurante_by_id(ambiente.restaurante_id)
                
                table_data.append({
                    "Data": reservation.data_reserva.strftime('%d/%m/%Y'),
                    "Hora": reservation.data_reserva.strftime('%H:%M'),
                    "Cliente": cliente.nome,
                    "Restaurante": restaurante.nome,
                    "Mesa": mesa.numero,
                    "Pessoas": reservation.numero_pessoas,
                    "Status": "✅ Confirmada" if reservation.status == 'confirmada' else "❌ Cancelada"
                })
            except:
                continue
        
        if table_data:
            # Ordenar por data e hora
            table_data.sort(key=lambda x: (x["Data"], x["Hora"]))
            
            import pandas as pd
            df = pd.DataFrame(table_data)
            st.dataframe(df, width='stretch', hide_index=True)
        
        st.divider()
        
        # Detalhes expandíveis
        st.subheader("📝 Detalhes das Reservas")
        
        for reservation in reservations:
            try:
                cliente = cliente_service.get_cliente_by_id(reservation.cliente_id)
                mesa = mesa_service.get_mesa_by_id(reservation.mesa_id)
                ambiente = ambiente_service.get_ambiente_by_id(mesa.ambiente_id)
                restaurante = restaurante_service.get_restaurante_by_id(ambiente.restaurante_id)
                
                status_emoji = "✅" if reservation.status == "confirmada" else "❌"
                
                with st.expander(
                    f"{status_emoji} {reservation.data_reserva.strftime('%H:%M')} - {cliente.nome} - {restaurante.nome}",
                    expanded=False
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Cliente:** {cliente.nome}")
                        st.write(f"**Email:** {cliente.email}")
                        st.write(f"**Telefone:** {cliente.telefone}")
                        st.write(f"**Restaurante:** {restaurante.nome}")
                        st.write(f"**Ambiente:** {ambiente.nome}")
                        st.write(f"**Mesa:** {mesa.numero}")
                        st.write(f"**Pessoas:** {reservation.numero_pessoas}")
                        st.write(f"**Status:** {reservation.status.upper()}")
                        if reservation.observacoes:
                            st.write(f"**Observações:** {reservation.observacoes}")
                    
                    with col2:
                        if reservation.status == "confirmada":
                            if st.button(f"🚫 Cancelar", key=f"cancel_res_{reservation.id}"):
                                if reserva_service.cancel_reserva(reservation.id):
                                    self.utils.show_success("Reserva cancelada com sucesso!")
                                    st.rerun()
                                else:
                                    self.utils.show_error("Erro ao cancelar reserva.")
            except Exception as e:
                continue
    
    def _render_clients(self):
        """Renderiza gerenciamento de clientes"""
        st.subheader("👥 Gerenciamento de Clientes")
        
        clients = cliente_service.get_all_clientes()
        
        if not clients:
            self.utils.show_info("Nenhum cliente cadastrado.")
            return
        
        # Estatísticas
        st.write(f"**Total de clientes:** {len(clients)}")
        
        # Lista de clientes
        for client in clients:
            reservas_cliente = reserva_service.get_reservas_by_cliente(client.id)
            reservas_ativas = [r for r in reservas_cliente if r.status == 'confirmada']
            
            with st.expander(f"👤 {client.nome}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Email:** {client.email}")
                    st.write(f"**Telefone:** {client.telefone}")
                    st.write(f"**Data de Cadastro:** {client.data_cadastro.strftime('%d/%m/%Y')}")
                    st.write(f"**Total de Reservas:** {len(reservas_cliente)}")
                    st.write(f"**Reservas Ativas:** {len(reservas_ativas)}")
                
                with col2:
                    # Botão de editar
                    if st.button(f"✏️ Editar", key=f"edit_client_{client.id}"):
                        st.session_state[f"editing_client_{client.id}"] = True
                        st.rerun()
                    
                    # Botão de excluir (apenas se não tiver reservas ativas)
                    if len(reservas_ativas) == 0:
                        if self.utils.create_confirmation_dialog(
                            "Excluir",
                            f"Tem certeza que deseja excluir o cliente {client.nome}?",
                            f"delete_client_{client.id}"
                        ):
                            if cliente_service.delete_cliente(client.id):
                                self.utils.show_success("Cliente excluído com sucesso!")
                                st.rerun()
                            else:
                                self.utils.show_error("Erro ao excluir cliente.")
                    else:
                        st.write("*Cliente com reservas ativas*")
                
                # Formulário de edição
                if st.session_state.get(f"editing_client_{client.id}", False):
                    st.divider()
                    st.write("**Editar Cliente:**")
                    
                    with st.form(f"edit_client_form_{client.id}"):
                        new_nome = st.text_input("Nome:", value=client.nome)
                        new_email = st.text_input("Email:", value=client.email)
                        new_telefone = st.text_input("Telefone:", value=client.telefone)
                        
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.form_submit_button("💾 Salvar", use_container_width=True):
                                if cliente_service.update_cliente(client.id, {
                                    'nome': new_nome,
                                    'email': new_email,
                                    'telefone': new_telefone
                                }):
                                    self.utils.show_success("Cliente atualizado com sucesso!")
                                    st.session_state[f"editing_client_{client.id}"] = False
                                    st.rerun()
                                else:
                                    self.utils.show_error("Erro ao atualizar cliente.")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                st.session_state[f"editing_client_{client.id}"] = False
                                st.rerun()
    
    def _render_reports(self):
        """Renderiza relatórios"""
        st.subheader("📊 Relatórios")
        
        report_type = st.selectbox(
            "Selecione o tipo de relatório:",
            [
                "Reservas por Período",
                "Ocupação por Restaurante",
                "Clientes Mais Ativos"
            ]
        )
        
        if report_type == "Reservas por Período":
            self._render_reservations_report()
        elif report_type == "Ocupação por Restaurante":
            self._render_occupancy_report()
        elif report_type == "Clientes Mais Ativos":
            self._render_top_clients_report()
    
    def _render_reservations_report(self):
        """Relatório de reservas por período"""
        st.subheader("Reservas por Período")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data inicial:", value=date.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("Data final:", value=date.today())
        
        if start_date <= end_date:
            # Buscar reservas no período
            all_reservations = []
            current_date = start_date
            
            while current_date <= end_date:
                current_datetime = datetime.combine(current_date, datetime.min.time())
                daily_reservations = reserva_service.get_reservas_by_data(current_datetime)
                all_reservations.extend(daily_reservations)
                current_date += timedelta(days=1)
            
            if all_reservations:
                # Preparar dados para gráfico
                reservations_by_date = {}
                reservations_by_status = {"confirmada": 0, "cancelada": 0}
                
                for reservation in all_reservations:
                    date_key = reservation.data_reserva.date()
                    if date_key not in reservations_by_date:
                        reservations_by_date[date_key] = 0
                    reservations_by_date[date_key] += 1
                    reservations_by_status[reservation.status] += 1
                
                # Métricas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Reservas", len(all_reservations))
                with col2:
                    st.metric("Confirmadas", reservations_by_status["confirmada"])
                with col3:
                    st.metric("Canceladas", reservations_by_status["cancelada"])
                
                # Gráfico de linha
                if reservations_by_date:
                    chart_data = pd.DataFrame(
                        list(reservations_by_date.items()),
                        columns=['Data', 'Reservas']
                    )
                    st.line_chart(chart_data.set_index('Data'))
            else:
                self.utils.show_info("Nenhuma reserva encontrada no período selecionado.")
        else:
            self.utils.show_error("Data inicial deve ser anterior à data final.")
    
    def _render_occupancy_report(self):
        """Relatório de ocupação por restaurante"""
        st.subheader("Ocupação por Restaurante")
        
        restaurants = restaurante_service.get_all_restaurantes()
        
        if not restaurants:
            self.utils.show_info("Nenhum restaurante cadastrado.")
            return
        
        # Data para análise
        analysis_date = st.date_input("Data para análise:", value=date.today())
        
        # Converter date para datetime
        analysis_datetime = datetime.combine(analysis_date, datetime.min.time())
        reservations = reserva_service.get_reservas_by_data(analysis_datetime)
        active_reservations = [r for r in reservations if r.status == 'confirmada']
        
        occupancy_data = []
        
        for restaurant in restaurants:
            # Contar mesas e capacidade total
            environments = ambiente_service.get_ambientes_by_restaurante(restaurant.id)
            total_tables = 0
            total_capacity = 0
            
            for env in environments:
                tables = mesa_service.get_mesas_by_ambiente(env.id)
                total_tables += len(tables)
                total_capacity += sum(table.capacidade for table in tables)
            
            # Contar reservas
            restaurant_reservations = []
            for reservation in active_reservations:
                mesa = mesa_service.get_mesa_by_id(reservation.mesa_id)
                ambiente = ambiente_service.get_ambiente_by_id(mesa.ambiente_id)
                if ambiente.restaurante_id == restaurant.id:
                    restaurant_reservations.append(reservation)
            
            occupied_tables = len(restaurant_reservations)
            occupied_capacity = sum(r.numero_pessoas for r in restaurant_reservations)
            
            occupancy_data.append({
                "Restaurante": restaurant.nome,
                "Total de Mesas": total_tables,
                "Mesas Ocupadas": occupied_tables,
                "% Ocupação Mesas": f"{(occupied_tables/total_tables*100):.1f}%" if total_tables > 0 else "0%",
                "Capacidade Total": total_capacity,
                "Pessoas": occupied_capacity,
                "% Ocupação Pessoas": f"{(occupied_capacity/total_capacity*100):.1f}%" if total_capacity > 0 else "0%"
            })
        
        if occupancy_data:
            df = pd.DataFrame(occupancy_data)
            st.dataframe(df, width='stretch')
        else:
            self.utils.show_info("Nenhum dado de ocupação disponível.")
    
    def _render_top_clients_report(self):
        """Relatório de clientes mais ativos"""
        st.subheader("Clientes Mais Ativos")
        
        clients = cliente_service.get_all_clientes()
        
        if not clients:
            self.utils.show_info("Nenhum cliente cadastrado.")
            return
        
        # Período para análise
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data inicial:", value=date.today() - timedelta(days=90))
        with col2:
            end_date = st.date_input("Data final:", value=date.today())
        
        if start_date <= end_date:
            client_data = []
            
            for client in clients:
                reservations = reserva_service.get_reservas_by_cliente(client.id)
                
                # Filtrar por período
                period_reservations = [
                    r for r in reservations
                    if start_date <= r.data_reserva.date() <= end_date
                ]
                
                confirmed_reservations = [r for r in period_reservations if r.status == 'confirmada']
                canceled_reservations = [r for r in period_reservations if r.status == 'cancelada']
                
                if period_reservations:  # Apenas clientes com reservas no período
                    client_data.append({
                        "Cliente": client.nome,
                        "Email": client.email,
                        "Total Reservas": len(period_reservations),
                        "Confirmadas": len(confirmed_reservations),
                        "Canceladas": len(canceled_reservations),
                        "Taxa Confirmação": f"{(len(confirmed_reservations)/len(period_reservations)*100):.1f}%"
                    })
            
            if client_data:
                # Ordenar por total de reservas
                client_data.sort(key=lambda x: x["Total Reservas"], reverse=True)
                
                # Mostrar top 10
                df = pd.DataFrame(client_data[:10])
                st.dataframe(df, width='stretch')
            else:
                self.utils.show_info("Nenhum cliente com reservas no período selecionado.")
        else:
            self.utils.show_error("Data inicial deve ser anterior à data final.")

    def _render_users(self):
        """Renderiza a gestão de utilizadores"""
        st.subheader("👥 Gestão de Utilizadores")
        
        tab1, tab2 = st.tabs(["Administradores", "Clientes"])
        
        with tab1:
            self._render_admin_management()
        
        with tab2:
            self._render_client_management()
    
    def _render_admin_management(self):
        """Renderiza gestão de administradores"""
        st.markdown("#### 👨‍💼 Gestão de Administradores")
        
        # Lista de administradores (mockup - pode ser expandido com base de dados)
        st.markdown("**Administradores Atuais:**")
        admins = [
            {"Username": "admin", "Status": "Ativo", "Criado": "2024-01-01"}
        ]
        
        df_admins = pd.DataFrame(admins)
        st.dataframe(df_admins, use_container_width=True)
        
        st.divider()
        
        # Formulário para adicionar novo administrador
        st.markdown("**Adicionar Novo Administrador:**")
        
        with st.form("add_admin"):
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("Username:", placeholder="novo_admin")
                new_password = st.text_input("Password:", type="password", placeholder="senha123")
            with col2:
                confirm_password = st.text_input("Confirmar Password:", type="password", placeholder="senha123")
                admin_role = st.selectbox("Tipo:", ["Super Admin", "Admin", "Moderador"])
            
            submit_admin = st.form_submit_button("✅ Criar Administrador", type="primary")
            
            if submit_admin:
                if not new_username or not new_password:
                    st.error("❌ Por favor, preencha todos os campos.")
                elif new_password != confirm_password:
                    st.error("❌ As palavras-passe não coincidem.")
                elif len(new_password) < 6:
                    st.error("❌ A palavra-passe deve ter pelo menos 6 caracteres.")
                else:
                    # Aqui seria implementada a lógica para criar o administrador
                    st.success(f"✅ Administrador '{new_username}' criado com sucesso!")
                    st.info("💡 Nota: Esta é uma implementação mockup. Em produção, seria criado na base de dados.")
    
    def _render_client_management(self):
        """Renderiza gestão de clientes"""
        st.markdown("#### 👤 Gestão de Clientes")
        
        # Tabs para diferentes ações
        tab1, tab2 = st.tabs(["📋 Listar Clientes", "➕ Adicionar Cliente"])
        
        with tab1:
            # Listar clientes existentes
            clientes = cliente_service.get_all_clientes()
            
            if clientes:
                st.markdown("**Clientes Registados:**")
                
                for cliente in clientes:
                    reservas = reserva_service.get_reservas_by_cliente(cliente.id)
                    total_reservas = len(reservas)
                    
                    with st.expander(f"👤 {cliente.nome} - {cliente.email}"):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**ID:** {cliente.id}")
                            st.write(f"**Nome:** {cliente.nome}")
                            st.write(f"**Email:** {cliente.email}")
                            st.write(f"**Telefone:** {cliente.telefone}")
                            st.write(f"**Total de Reservas:** {total_reservas}")
                        
                        with col2:
                            # Botão Editar
                            if st.button("✏️ Editar", key=f"edit_client_{cliente.id}"):
                                st.session_state[f"editing_client_{cliente.id}"] = True
                                st.rerun()
                        
                        with col3:
                            # Botão Excluir (apenas se não tiver reservas ativas)
                            reservas_ativas = [r for r in reservas if r.status == 'confirmada' and r.data_reserva > datetime.now()]
                            
                            if len(reservas_ativas) == 0:
                                if st.button("🗑️ Excluir", key=f"delete_client_{cliente.id}", type="secondary"):
                                    if cliente_service.delete_cliente(cliente.id):
                                        st.success(f"✅ Cliente {cliente.nome} excluído com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao excluir cliente.")
                            else:
                                st.warning(f"⚠️ {len(reservas_ativas)} reserva(s) ativa(s)")
                        
                        # Formulário de edição (se ativado)
                        if st.session_state.get(f"editing_client_{cliente.id}", False):
                            st.markdown("---")
                            st.markdown("**Editar Dados:**")
                            
                            with st.form(f"edit_form_{cliente.id}"):
                                edit_nome = st.text_input("Nome:", value=cliente.nome, key=f"edit_nome_{cliente.id}")
                                edit_email = st.text_input("Email:", value=cliente.email, key=f"edit_email_{cliente.id}")
                                edit_telefone = st.text_input("Telefone:", value=cliente.telefone, key=f"edit_telefone_{cliente.id}")
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    save_changes = st.form_submit_button("✅ Salvar", type="primary")
                                with col_cancel:
                                    cancel_edit = st.form_submit_button("❌ Cancelar")
                            
                            if save_changes:
                                if edit_nome and edit_email and edit_telefone:
                                    updated_cliente = cliente_service.update_cliente_dados(
                                        cliente.id, edit_nome, edit_email, edit_telefone
                                    )
                                    if updated_cliente:
                                        st.success("✅ Cliente atualizado com sucesso!")
                                        st.session_state[f"editing_client_{cliente.id}"] = False
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao atualizar cliente.")
                                else:
                                    st.error("❌ Preencha todos os campos.")
                            
                            if cancel_edit:
                                st.session_state[f"editing_client_{cliente.id}"] = False
                                st.rerun()
            else:
                st.info("📝 Nenhum cliente registado.")
        
        with tab2:
            # Formulário para adicionar novo cliente
            st.markdown("**Adicionar Novo Cliente:**")
        
        with st.form("add_client"):
            col1, col2 = st.columns(2)
            with col1:
                client_nome = st.text_input("Nome completo:", placeholder="João Silva")
                client_email = st.text_input("Email:", placeholder="joao.silva@email.com")
            with col2:
                client_telefone = st.text_input("Telefone:", placeholder="+351 XXX XXX XXX")
            
            submit_client = st.form_submit_button("✅ Criar Cliente", type="primary")
            
            if submit_client:
                if not client_nome or not client_email or not client_telefone:
                    st.error("❌ Por favor, preencha todos os campos.")
                else:
                    try:
                        # Criar cliente
                        novo_cliente = cliente_service.create_cliente(client_nome, client_email, client_telefone)
                        if novo_cliente:
                            st.success(f"✅ Cliente '{client_nome}' criado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao criar cliente.")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")


def render_admin_page():
    """Função principal para renderizar a página administrativa"""
    page = AdminPage()
    page.render()