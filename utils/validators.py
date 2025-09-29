import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from typing import Optional, Tuple
from datetime import datetime, date


class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    pass


class DataValidator:
    """Classe para validação de dados"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Valida formato de email
        
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if not email or not email.strip():
            return False, "Email é obrigatório"
        
        try:
            validate_email(email.strip())
            return True, ""
        except EmailNotValidError as e:
            return False, f"Email inválido: {str(e)}"
    
    @staticmethod
    def validate_phone(phone: str, country: str = "PT") -> Tuple[bool, str]:
        """
        Valida formato de telefone
        
        Args:
            phone: Número de telefone
            country: Código do país (padrão: PT)
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if not phone or not phone.strip():
            return False, "Telemóvel é obrigatório"
        
        try:
            parsed_phone = phonenumbers.parse(phone, country)
            if phonenumbers.is_valid_number(parsed_phone):
                return True, ""
            else:
                return False, "Número de telemóvel inválido"
        except phonenumbers.NumberParseException:
            return False, "Formato de telemóvel inválido"
    
    @staticmethod
    def validate_name(name: str, min_length: int = 2, max_length: int = 100) -> Tuple[bool, str]:
        """
        Valida nome
        
        Args:
            name: Nome a ser validado
            min_length: Comprimento mínimo
            max_length: Comprimento máximo
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if not name or not name.strip():
            return False, "Nome é obrigatório"
        
        name = name.strip()
        
        if len(name) < min_length:
            return False, f"Nome deve ter pelo menos {min_length} caracteres"
        
        if len(name) > max_length:
            return False, f"Nome deve ter no máximo {max_length} caracteres"
        
        # Verificar se contém apenas letras, espaços e alguns caracteres especiais
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-\'\.]+$", name):
            return False, "Nome contém caracteres inválidos"
        
        return True, ""
    
    @staticmethod
    def validate_capacity(capacity: int, min_capacity: int = 1, max_capacity: int = 20) -> Tuple[bool, str]:
        """
        Valida capacidade de mesa ou número de pessoas
        
        Args:
            capacity: Capacidade
            min_capacity: Capacidade mínima
            max_capacity: Capacidade máxima
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if capacity is None:
            return False, "Capacidade é obrigatória"
        
        if not isinstance(capacity, int) or capacity < min_capacity:
            return False, f"Capacidade deve ser pelo menos {min_capacity}"
        
        if capacity > max_capacity:
            return False, f"Capacidade não pode exceder {max_capacity}"
        
        return True, ""
    
    @staticmethod
    def validate_reservation_date(reservation_date: datetime) -> Tuple[bool, str]:
        """
        Valida data de reserva
        
        Args:
            reservation_date: Data e hora da reserva
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if not reservation_date:
            return False, "Data da reserva é obrigatória"
        
        now = datetime.now()
        
        # Não permitir reservas no passado
        if reservation_date < now:
            return False, "Não é possível fazer reservas para datas passadas"
        
        # Não permitir reservas com mais de 90 dias de antecedência
        max_advance_days = 90
        if (reservation_date - now).days > max_advance_days:
            return False, f"Reservas podem ser feitas com até {max_advance_days} dias de antecedência"
        
        return True, ""
    
    @staticmethod
    def validate_table_number(table_number: str) -> Tuple[bool, str]:
        """
        Valida número da mesa
        
        Args:
            table_number: Número da mesa
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if not table_number or not table_number.strip():
            return False, "Número da mesa é obrigatório"
        
        table_number = table_number.strip()
        
        if len(table_number) > 10:
            return False, "Número da mesa deve ter no máximo 10 caracteres"
        
        # Permitir letras, números e alguns caracteres especiais
        if not re.match(r"^[a-zA-Z0-9\-_]+$", table_number):
            return False, "Número da mesa contém caracteres inválidos"
        
        return True, ""



class TextUtils:
    """Utilitários para manipulação de texto"""
    
    @staticmethod
    def capitalize_name(name: str) -> str:
        """
        Capitaliza nome próprio
        
        Args:
            name: Nome a ser capitalizado
            
        Returns:
            str: Nome capitalizado
        """
        if not name:
            return ""
        
        # Lista de preposições que não devem ser capitalizadas
        prepositions = ['de', 'da', 'do', 'das', 'dos', 'e', 'em', 'na', 'no', 'nas', 'nos']
        
        words = name.strip().lower().split()
        capitalized_words = []
        
        for i, word in enumerate(words):
            if i == 0 or word not in prepositions:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word)
        
        return ' '.join(capitalized_words)
    
    @staticmethod
    def clean_string(text: str) -> str:
        """
        Remove espaços extras e caracteres especiais
        
        Args:
            text: Texto a ser limpo
            
        Returns:
            str: Texto limpo
        """
        if not text:
            return ""
        
        # Remove espaços extras
        cleaned = ' '.join(text.split())
        
        return cleaned.strip()
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Trunca texto se necessário
        
        Args:
            text: Texto a ser truncado
            max_length: Comprimento máximo
            suffix: Sufixo para texto truncado
            
        Returns:
            str: Texto truncado
        """
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix