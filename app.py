import streamlit as st
import logging
from database.connection import db_manager
from config import Config

# Importar páginas
from pages.client import ClientePage
from pages.admin import AdminPage

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def initialize_app():
    """Inicializa configurações da aplicação"""
    logger.info("Aplicação unificada inicializada com sucesso")
    
    # Configurar página
    st.set_page_config(
        page_title="Sistema de Gestão de Restaurantes",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # CSS completo para ocultar elementos nativos do Streamlit e estilizar
    hide_streamlit_elements = """
    <style>
    /* Ocultar elementos nativos do Streamlit */
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    header[data-testid="stHeader"] {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stActionButton {visibility: hidden !important;}
    .stToolbar {display: none !important;}
    
    /* Ocultar sidebar nativa do Streamlit */
    section[data-testid="stSidebar"] {display: none !important;}
    .css-1d391kg {display: none !important;}
    .stSidebar {display: none !important;}
    
    /* Ajustar layout principal */
    .main .block-container {
        padding-top: 1rem;
        max-width: 100%;
    }
    
    /* Header principal do sistema */
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
    
    /* CSS limpo - estilos desnecessários removidos */
    </style>
    """
    st.markdown(hide_streamlit_elements, unsafe_allow_html=True)


def render_system_header():
    """Renderiza o header principal do sistema"""
    st.markdown("""
    <div class="system-header">
        <h1>🍽️ Sistema de Gestão de Restaurantes</h1>
        <div class="subtitle">Plataforma completa para gestão de reservas e operações</div>
    </div>
    """, unsafe_allow_html=True)

def render_login_page():
    """Renderiza a página de login unificada"""
    
    # Header do sistema
    render_system_header()
    
    # Container centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Escolha o tipo de acesso:")
        
        # Seleção do tipo de utilizador
        user_type = st.radio(
            "Selecione o tipo de acesso:",
            ["👤 Cliente", "👨‍💼 Administrador"],
            key="login_user_type",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.divider()
        
        if user_type == "👤 Cliente":
            render_client_login()
        else:
            render_admin_login()


def render_client_login():
    """Renderiza login para clientes"""
    st.markdown("#### 👤 Acesso de Cliente")
    st.info("💡 Como cliente, pode fazer reservas e gerir as suas reservas existentes.")
    
    with st.form("client_login"):
        email = st.text_input("📧 Email:", placeholder="seu.email@exemplo.com")
        telefone = st.text_input("📱 Telefone:", placeholder="+351 XXX XXX XXX")
        
        col1, col2 = st.columns(2)
        with col1:
            login_submitted = st.form_submit_button("🚀 Entrar", type="primary")
        with col2:
            register_mode = st.form_submit_button("📝 Registar Novo Cliente")
    
    # Processar login fora do formulário
    if login_submitted:
        if email and telefone:
            # Validar cliente existente
            from services import cliente_service
            cliente = cliente_service.get_cliente_by_email(email)
            
            if cliente and cliente.telefone == telefone:
                st.session_state["is_logged_in"] = True
                st.session_state["logged_user_type"] = "client"
                st.session_state["logged_user_data"] = {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "email": cliente.email,
                    "telefone": cliente.telefone
                }
                st.success(f"✅ Bem-vindo, {cliente.nome}!")
                st.rerun()
            else:
                st.error("❌ Cliente não encontrado ou dados incorrectos.")
        else:
            st.error("❌ Por favor, preencha todos os campos.")
    
    if register_mode:
        st.session_state["show_register"] = True
        st.rerun()


def render_admin_login():
    """Renderiza login para administradores"""
    st.markdown("#### 👨‍💼 Acesso de Administrador")
    st.info("💡 Como administrador, tem acesso completo ao sistema de gestão.")
    
    with st.form("admin_login"):
        username = st.text_input("👤 Utilizador:", placeholder="admin")
        password = st.text_input("🔒 Palavra-passe:", type="password", placeholder="senha")
        
        login_submitted = st.form_submit_button("🚀 Entrar", type="primary")
    
    # Processar login fora do formulário
    if login_submitted:
        # Credenciais fixas para administrador
        if username == "admin" and password == "admin123":
            st.session_state["is_logged_in"] = True
            st.session_state["logged_user_type"] = "admin"
            st.session_state["logged_user_data"] = {
                "username": username,
                "role": "administrator"
            }
            st.success("✅ Login de administrador realizado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Credenciais de administrador incorrectas.")


def render_client_register():
    """Renderiza formulário de registo de cliente"""
    st.markdown("#### 📝 Registar Novo Cliente")
    
    with st.form("client_register"):
        nome = st.text_input("👤 Nome completo:", placeholder="João Silva")
        email = st.text_input("📧 Email:", placeholder="joao.silva@exemplo.com")
        telefone = st.text_input("📱 Telefone:", placeholder="+351 XXX XXX XXX")
        
        col1, col2 = st.columns(2)
        with col1:
            register_submitted = st.form_submit_button("✅ Registar", type="primary")
        with col2:
            back_to_login = st.form_submit_button("⬅️ Voltar ao Login")
    
    # Processar registo fora do formulário
    if register_submitted:
        if nome and email and telefone:
            from services import cliente_service
            try:
                cliente = cliente_service.create_cliente(nome, email, telefone)
                if cliente:
                    st.success(f"✅ Cliente {nome} registado com sucesso!")
                    st.session_state["show_register"] = False
                    st.session_state["is_logged_in"] = True
                    st.session_state["logged_user_type"] = "client"
                    st.session_state["logged_user_data"] = {
                        "id": cliente.id,
                        "nome": cliente.nome,
                        "email": cliente.email,
                        "telefone": cliente.telefone
                    }
                    st.rerun()
                else:
                    st.error("❌ Erro ao registar cliente.")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
        else:
            st.error("❌ Por favor, preencha todos os campos.")
    
    if back_to_login:
        st.session_state["show_register"] = False
        st.rerun()


def main():
    """Função principal da aplicação"""
    initialize_app()
    
    # Verificar se há registo pendente
    if st.session_state.get("show_register", False):
        render_client_register()
        return
    
    # Verificar se o utilizador está logado
    if not st.session_state.get("is_logged_in", False):
        render_login_page()
        return
    
    # Utilizador logado - mostrar interface apropriada
    user_type = st.session_state.get("logged_user_type")
    
    if user_type == "client":
        # Interface do cliente
        # Definir variáveis para compatibilidade com ClientePage
        user_data = st.session_state.get("logged_user_data", {})
        if "id" in user_data:
            st.session_state.cliente_id = user_data["id"]
            st.session_state.cliente_nome = user_data.get("nome", "Cliente")
        client_page = ClientePage()
        client_page.render()
        
    elif user_type == "admin":
        # Interface do administrador
        admin_page = AdminPage()
        admin_page.render()
    
    else:
        st.error("❌ Tipo de utilizador inválido.")
        st.session_state["is_logged_in"] = False
        st.rerun()


if __name__ == "__main__":
    main()