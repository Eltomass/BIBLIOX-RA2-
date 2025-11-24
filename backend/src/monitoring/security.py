"""
Sistema de Validación de Seguridad para BiblioX
IE6: Integración de protocolos de seguridad y uso responsable
"""

import re
from typing import Optional


class SecurityValidator:
    """
    Validador de seguridad para prevenir ataques y uso malicioso del agente.
    """
    
    # Patrones sospechosos de prompt injection
    INJECTION_PATTERNS = [
        r'ignore\s+(previous|all)\s+instructions',
        r'disregard\s+(previous|all)\s+instructions',
        r'you\s+are\s+now',
        r'act\s+as\s+(if|a|an)',
        r'new\s+instructions:',
        r'system\s+message:',
        r'override\s+instructions',
        r'</system>',
        r'<\|im_start\|>',
        r'<\|im_end\|>',
    ]
    
    # Patrones de información sensible (PII)
    PII_PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'rut': r'\b\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]\b',
    }
    
    @staticmethod
    def validate_input(user_input: str) -> tuple[bool, Optional[str]]:
        """
        Valida que el input del usuario no contenga intentos de injection.
        
        Returns:
            (is_valid, error_message)
        """
        user_input_lower = user_input.lower()
        
        for pattern in SecurityValidator.INJECTION_PATTERNS:
            if re.search(pattern, user_input_lower):
                return False, "Input potencialmente peligroso detectado"
        
        # Validar longitud
        if len(user_input) > 5000:
            return False, "Input demasiado largo (máximo 5000 caracteres)"
        
        return True, None
    
    @staticmethod
    def sanitize_pii(text: str) -> str:
        """
        Elimina información personal identificable de los logs.
        
        Returns:
            Texto con PII anonimizada
        """
        sanitized = text
        
        # Reemplazar emails
        sanitized = re.sub(
            SecurityValidator.PII_PATTERNS['email'],
            '[EMAIL_REDACTED]',
            sanitized
        )
        
        # Reemplazar teléfonos
        sanitized = re.sub(
            SecurityValidator.PII_PATTERNS['phone'],
            '[PHONE_REDACTED]',
            sanitized
        )
        
        # Reemplazar RUTs
        sanitized = re.sub(
            SecurityValidator.PII_PATTERNS['rut'],
            '[RUT_REDACTED]',
            sanitized
        )
        
        return sanitized
    
    @staticmethod
    def check_content_safety(response: str) -> tuple[bool, Optional[str]]:
        """
        Verifica que la respuesta no contenga contenido inapropiado.
        
        Returns:
            (is_safe, warning_message)
        """
        # Palabras prohibidas básicas (expandir según necesidad)
        forbidden_words = ['contraseña', 'password', 'token', 'api_key', 'secret']
        
        response_lower = response.lower()
        for word in forbidden_words:
            if word in response_lower:
                return False, f"Respuesta contiene información sensible: {word}"
        
        return True, None


class RateLimiter:
    """
    Limitador de tasa de requests para prevenir abuso.
    """
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_log = {}
    
    def check_rate_limit(self, user_id: str) -> tuple[bool, Optional[str]]:
        """
        Verifica si el usuario ha excedido el límite de requests.
        
        Returns:
            (is_allowed, error_message)
        """
        import time
        
        current_time = time.time()
        
        # Limpiar requests antiguos
        if user_id in self.request_log:
            self.request_log[user_id] = [
                t for t in self.request_log[user_id]
                if current_time - t < self.window_seconds
            ]
        else:
            self.request_log[user_id] = []
        
        # Verificar límite
        if len(self.request_log[user_id]) >= self.max_requests:
            return False, f"Límite de {self.max_requests} requests por {self.window_seconds}s excedido"
        
        # Registrar request
        self.request_log[user_id].append(current_time)
        
        return True, None


# Instancias globales
_rate_limiter = RateLimiter(max_requests=20, window_seconds=60)


def get_rate_limiter() -> RateLimiter:
    """Retorna la instancia global del rate limiter."""
    return _rate_limiter
