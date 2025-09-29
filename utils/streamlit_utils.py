import streamlit as st
from typing import Any, Dict, List, Optional
from datetime import datetime, time


class StreamlitUtils:
    """Utilitários para interface Streamlit"""
    
    @staticmethod
    def show_success(message: str):
        """Exibe mensagem de sucesso"""
        st.success(f"✅ {message}")
    
    @staticmethod
    def show_error(message: str):
        """Exibe mensagem de erro"""
        st.error(f"❌ {message}")
    
    @staticmethod
    def show_warning(message: str):
        """Exibe mensagem de aviso"""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def show_info(message: str):
        """Exibe mensagem informativa"""
        st.info(f"ℹ️ {message}")
    

    

    

    

    
    @staticmethod
    def create_confirmation_dialog(title: str, message: str, key: str) -> bool:
        """
        Cria um diálogo de confirmação
        
        Args:
            title: Título do diálogo
            message: Mensagem de confirmação
            key: Chave única para o diálogo
            
        Returns:
            bool: True se confirmado
        """
        if f"confirm_{key}" not in st.session_state:
            st.session_state[f"confirm_{key}"] = False
        
        if st.button(title, key=f"btn_{key}"):
            st.session_state[f"confirm_{key}"] = True
        
        if st.session_state[f"confirm_{key}"]:
            st.warning(message)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Confirmar", key=f"confirm_yes_{key}"):
                    st.session_state[f"confirm_{key}"] = False
                    return True
            
            with col2:
                if st.button("Cancelar", key=f"confirm_no_{key}"):
                    st.session_state[f"confirm_{key}"] = False
        
        return False
