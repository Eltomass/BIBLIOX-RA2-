"""
Sistema de Métricas de Observabilidad para BiblioX
IE1: Métricas de precisión, consistencia y errores
IE2: Métricas de latencia y uso de recursos
"""

import time
import psutil
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import threading


class MetricsCollector:
    """
    Recolector centralizado de métricas para el agente BiblioX.
    Captura métricas de precisión, latencia, recursos y errores.
    """
    
    def __init__(self):
        self.metrics_data = {
            'requests': [],
            'tools': defaultdict(list),
            'rag': defaultdict(list),
            'errors': [],
            'resources': []
        }
        self.current_request = None
        self.lock = threading.Lock()
        self.process = psutil.Process(os.getpid())
        
    def start_request(self, trace_id: str, query: str, session_id: str = "default"):
        """Inicia el tracking de un nuevo request."""
        with self.lock:
            self.current_request = {
                'trace_id': trace_id,
                'query': query,
                'session_id': session_id,
                'start_time': time.time(),
                'start_timestamp': datetime.now().isoformat(),
                'components': {},
                'tools_used': [],
                'errors': [],
                'resources_start': self._capture_resources()
            }
    
    def end_request(self, response: str, status: str = "success"):
        """Finaliza el tracking de un request."""
        if not self.current_request:
            return
            
        with self.lock:
            end_time = time.time()
            self.current_request['end_time'] = end_time
            self.current_request['end_timestamp'] = datetime.now().isoformat()
            self.current_request['response'] = response
            self.current_request['status'] = status
            self.current_request['total_latency'] = end_time - self.current_request['start_time']
            self.current_request['resources_end'] = self._capture_resources()
            
            # Calcular uso de recursos
            self.current_request['resource_usage'] = {
                'cpu_percent': self.current_request['resources_end']['cpu_percent'],
                'memory_mb': (
                    self.current_request['resources_end']['memory_rss_mb'] - 
                    self.current_request['resources_start']['memory_rss_mb']
                )
            }
            
            # Guardar request completo
            self.metrics_data['requests'].append(self.current_request.copy())
            self.current_request = None
    
    def track_component(self, component_name: str, start_time: float, end_time: float, 
                       metadata: Optional[Dict] = None):
        """Registra el tiempo de ejecución de un componente."""
        if not self.current_request:
            return
            
        latency = end_time - start_time
        component_data = {
            'latency': latency,
            'start_time': start_time,
            'end_time': end_time
        }
        
        if metadata:
            component_data.update(metadata)
        
        with self.lock:
            self.current_request['components'][component_name] = component_data
    
    def track_tool(self, tool_name: str, latency: float, success: bool, 
                   input_data: str = "", output_data: str = ""):
        """Registra el uso de una herramienta del agente."""
        tool_data = {
            'tool_name': tool_name,
            'latency': latency,
            'success': success,
            'input': input_data[:200],  # Limitar tamaño
            'output': output_data[:200],
            'timestamp': datetime.now().isoformat()
        }
        
        with self.lock:
            self.metrics_data['tools'][tool_name].append(tool_data)
            if self.current_request:
                self.current_request['tools_used'].append(tool_data)
    
    def track_rag(self, component: str, latency: float, metadata: Optional[Dict] = None):
        """Registra métricas del sistema RAG."""
        rag_data = {
            'component': component,
            'latency': latency,
            'timestamp': datetime.now().isoformat()
        }
        
        if metadata:
            rag_data.update(metadata)
        
        with self.lock:
            self.metrics_data['rag'][component].append(rag_data)
    
    def track_error(self, error_type: str, error_message: str, component: str):
        """Registra un error."""
        error_data = {
            'type': error_type,
            'message': error_message,
            'component': component,
            'timestamp': datetime.now().isoformat()
        }
        
        with self.lock:
            self.metrics_data['errors'].append(error_data)
            if self.current_request:
                self.current_request['errors'].append(error_data)
    
    def _capture_resources(self) -> Dict[str, float]:
        """Captura el uso actual de recursos del sistema."""
        try:
            return {
                'cpu_percent': self.process.cpu_percent(interval=0.1),
                'memory_rss_mb': self.process.memory_info().rss / 1024 / 1024,
                'memory_percent': self.process.memory_percent(),
                'timestamp': time.time()
            }
        except:
            return {
                'cpu_percent': 0,
                'memory_rss_mb': 0,
                'memory_percent': 0,
                'timestamp': time.time()
            }
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Genera estadísticas resumidas de todas las métricas."""
        with self.lock:
            requests = self.metrics_data['requests']
            errors = self.metrics_data['errors']
            
            if not requests:
                return {
                    'total_requests': 0,
                    'successful_requests': 0,
                    'error_rate': 0,
                    'total_errors': 0,
                    'avg_latency': 0,
                    'min_latency': 0,
                    'max_latency': 0,
                    'p50_latency': 0,
                    'p95_latency': 0,
                    'p99_latency': 0,
                    'total_tools_used': 0,
                    'unique_tools': 0,
                    'tool_usage': {},
                    'most_used_tool': None,
                    'avg_cpu_percent': 0,
                    'avg_memory_mb': 0
                }
            
            # Latencias
            latencies = [r['total_latency'] for r in requests]
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            
            # Tasa de éxito
            successful = sum(1 for r in requests if r['status'] == 'success')
            
            # Herramientas
            all_tools_used = []
            for r in requests:
                all_tools_used.extend([t['tool_name'] for t in r.get('tools_used', [])])
            
            tool_counts = defaultdict(int)
            for tool in all_tools_used:
                tool_counts[tool] += 1
            
            return {
                'total_requests': len(requests),
                'successful_requests': successful,
                'error_rate': (len(requests) - successful) / len(requests) if requests else 0,
                'total_errors': len(errors),
                
                # Latencia
                'avg_latency': sum(latencies) / n if n > 0 else 0,
                'min_latency': min(latencies) if latencies else 0,
                'max_latency': max(latencies) if latencies else 0,
                'p50_latency': latencies_sorted[n // 2] if n > 0 else 0,
                'p95_latency': latencies_sorted[int(n * 0.95)] if n > 0 else 0,
                'p99_latency': latencies_sorted[int(n * 0.99)] if n > 0 else 0,
                
                # Herramientas
                'total_tools_used': len(all_tools_used),
                'unique_tools': len(tool_counts),
                'tool_usage': dict(tool_counts),
                'most_used_tool': max(tool_counts.items(), key=lambda x: x[1])[0] if tool_counts else None,
                
                # Recursos
                'avg_cpu_percent': sum(r['resource_usage']['cpu_percent'] for r in requests) / n if n > 0 else 0,
                'avg_memory_mb': sum(r['resource_usage']['memory_mb'] for r in requests) / n if n > 0 else 0
            }
    
    def get_component_stats(self, component_name: str) -> Dict[str, Any]:
        """Obtiene estadísticas de un componente específico."""
        with self.lock:
            latencies = []
            for req in self.metrics_data['requests']:
                if component_name in req.get('components', {}):
                    latencies.append(req['components'][component_name]['latency'])
            
            if not latencies:
                return {
                    'component': component_name,
                    'count': 0,
                    'avg_latency': 0
                }
            
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            
            return {
                'component': component_name,
                'count': n,
                'avg_latency': sum(latencies) / n,
                'min_latency': min(latencies),
                'max_latency': max(latencies),
                'p50_latency': latencies_sorted[n // 2],
                'p95_latency': latencies_sorted[int(n * 0.95)] if n > 0 else 0
            }
    
    def save_to_file(self, filepath: str):
        """Guarda todas las métricas en un archivo JSON."""
        with self.lock:
            data_to_save = {
                'summary': self.get_summary_stats(),
                'timestamp': datetime.now().isoformat(),
                'requests': self.metrics_data['requests'][-100:],  # Últimos 100 requests
                'errors': self.metrics_data['errors'][-50:],  # Últimos 50 errores
                'tool_stats': {
                    tool: {
                        'count': len(data),
                        'avg_latency': sum(d['latency'] for d in data) / len(data) if data else 0,
                        'success_rate': sum(1 for d in data if d['success']) / len(data) if data else 0
                    }
                    for tool, data in self.metrics_data['tools'].items()
                }
            }
            
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    def reset(self):
        """Resetea todas las métricas (útil para testing)."""
        with self.lock:
            self.metrics_data = {
                'requests': [],
                'tools': defaultdict(list),
                'rag': defaultdict(list),
                'errors': [],
                'resources': []
            }
            self.current_request = None


# Instancia global
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Retorna la instancia global del recolector de métricas."""
    return _metrics_collector
