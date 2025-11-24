"""
Sistema de Logging Estructurado para BiblioX
IE3: Análisis de registros y trazabilidad
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


class StructuredLogger:
    """
    Logger estructurado que genera logs en formato JSON para análisis.
    Permite trazabilidad completa del flujo de ejecución del agente.
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Configurar logger de Python
        self.logger = logging.getLogger('bibliox')
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para archivo JSON
        json_handler = logging.FileHandler(
            os.path.join(log_dir, 'agent.log'),
            encoding='utf-8'
        )
        json_handler.setLevel(logging.DEBUG)
        
        # Handler para consola (solo errores)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        self.logger.addHandler(json_handler)
        self.logger.addHandler(console_handler)
        
        self.current_trace_id = None
    
    def generate_trace_id(self) -> str:
        """Genera un ID único para trazabilidad."""
        return str(uuid.uuid4())[:8]
    
    def set_trace_id(self, trace_id: str):
        """Establece el trace ID actual."""
        self.current_trace_id = trace_id
    
    def _log(self, level: str, event: str, data: Optional[Dict[str, Any]] = None):
        """Método interno para logging estructurado."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'event': event,
            'trace_id': self.current_trace_id or 'unknown'
        }
        
        if data:
            log_entry['data'] = data
        
        # Log como JSON
        log_line = json.dumps(log_entry, ensure_ascii=False)
        
        if level == 'DEBUG':
            self.logger.debug(log_line)
        elif level == 'INFO':
            self.logger.info(log_line)
        elif level == 'WARNING':
            self.logger.warning(log_line)
        elif level == 'ERROR':
            self.logger.error(log_line)
        elif level == 'CRITICAL':
            self.logger.critical(log_line)
    
    def debug(self, event: str, data: Optional[Dict] = None):
        """Log nivel DEBUG."""
        self._log('DEBUG', event, data)
    
    def info(self, event: str, data: Optional[Dict] = None):
        """Log nivel INFO."""
        self._log('INFO', event, data)
    
    def warning(self, event: str, data: Optional[Dict] = None):
        """Log nivel WARNING."""
        self._log('WARNING', event, data)
    
    def error(self, event: str, data: Optional[Dict] = None):
        """Log nivel ERROR."""
        self._log('ERROR', event, data)
    
    def critical(self, event: str, data: Optional[Dict] = None):
        """Log nivel CRITICAL."""
        self._log('CRITICAL', event, data)
    
    # Métodos específicos para el agente ReAct
    
    def log_request_start(self, trace_id: str, query: str, session_id: str):
        """Registra el inicio de un request."""
        self.set_trace_id(trace_id)
        self.info('request_start', {
            'query': query,
            'session_id': session_id
        })
    
    def log_request_end(self, response: str, status: str, latency: float):
        """Registra el fin de un request."""
        self.info('request_end', {
            'response_length': len(response),
            'status': status,
            'latency': latency
        })
    
    def log_thought(self, thought: str):
        """Registra un pensamiento del agente (ReAct)."""
        self.debug('agent_thought', {
            'thought': thought[:500]  # Limitar tamaño
        })
    
    def log_action(self, tool_name: str, tool_input: str):
        """Registra una acción del agente (ReAct)."""
        self.info('agent_action', {
            'tool': tool_name,
            'input': tool_input[:200]
        })
    
    def log_observation(self, tool_name: str, result: str, latency: float):
        """Registra una observación del agente (ReAct)."""
        self.info('agent_observation', {
            'tool': tool_name,
            'result_length': len(result),
            'latency': latency
        })
    
    def log_final_answer(self, answer: str):
        """Registra la respuesta final del agente."""
        self.info('agent_final_answer', {
            'answer_length': len(answer)
        })
    
    def log_tool_execution(self, tool_name: str, success: bool, latency: float, error: str = ""):
        """Registra la ejecución de una herramienta."""
        self.info('tool_execution', {
            'tool': tool_name,
            'success': success,
            'latency': latency,
            'error': error if error else None
        })
    
    def log_memory_operation(self, operation: str, data: Optional[Dict] = None):
        """Registra operaciones de memoria."""
        self.debug('memory_operation', {
            'operation': operation,
            'data': data
        })
    
    def log_rag_operation(self, component: str, latency: float, metadata: Optional[Dict] = None):
        """Registra operaciones RAG."""
        log_data = {
            'component': component,
            'latency': latency
        }
        if metadata:
            log_data.update(metadata)
        
        self.info('rag_operation', log_data)
    
    def log_error(self, component: str, error_type: str, error_message: str):
        """Registra un error."""
        self.error('error_occurred', {
            'component': component,
            'error_type': error_type,
            'message': error_message
        })


# Instancia global
_logger = None


def get_logger(log_dir: str = "logs") -> StructuredLogger:
    """Retorna la instancia global del logger estructurado."""
    global _logger
    if _logger is None:
        _logger = StructuredLogger(log_dir)
    return _logger
