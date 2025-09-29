import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações da aplicação"""
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///restaurant_management.db')
    
    # App
    APP_TITLE = "Sistema de Gestão de Restaurantes"
    APP_ICON = "🍽️"
    
    # Page config
    PAGE_CONFIG = {
        "page_title": APP_TITLE,
        "page_icon": APP_ICON,
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    # Time slots for reservations
    TIME_SLOTS = [
        "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
        "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"
    ]