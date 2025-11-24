"""
IL2 - API de Agente Funcional con Memoria y Herramientas

IE2: Integración de frameworks (LangChain)
IE3: Memoria de contenido
IE4: Recuperación de contexto semántico
IE5: Planificación de tareas
IE6: Toma de decisiones adaptativas
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import time

# Importar el agente y sus dependencias
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents.agent import get_agent
from monitoring.metrics import get_metrics_collector
from monitoring.logger import get_logger
from monitoring.security import SecurityValidator, get_rate_limiter

# Base de Ollama y modelo LLM a utilizar
OLLAMA_URL = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")

app = FastAPI(
	title="BiblioX Agent API",
	description="API del agente funcional con memoria, herramientas y planificación",
	version="2.0"
)

# CORS abierto para permitir pruebas desde CRA en localhost
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Instancia global del agente
agent = get_agent()

# Sistema de observabilidad
metrics = get_metrics_collector()
logger = get_logger("backend/logs")
rate_limiter = get_rate_limiter()

class ChatRequest(BaseModel):
	"""Payload de entrada del endpoint de chat."""
	question: str
	session_id: str = "default"

class ChatResponse(BaseModel):
	"""Respuesta con el texto del asistente."""
	answer: str

class PlanRequest(BaseModel):
	"""Request para planificar una tarea."""
	objective: str

class PlanResponse(BaseModel):
	"""Respuesta con el plan generado."""
	plan: list
	objective: str


@app.get("/")
async def root():
	"""Endpoint raíz con información de la API."""
	return {
		"message": "BiblioX Agent API v2.0",
		"description": "Agente funcional con memoria, herramientas y planificación",
		"endpoints": {
			"/api/chat": "Chat con el agente",
			"/api/plan": "Planificar tareas",
			"/api/tools": "Listar herramientas disponibles",
			"/api/memory": "Consultar memoria del agente"
		}
	}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
	"""
	IE2, IE3, IE4, IE6: Endpoint de chat con agente funcional
	
	Características:
	- Usa memoria conversacional (IE3, IE4)
	- Ejecuta herramientas automáticamente (IE2)
	- Toma decisiones adaptativas (IE6)
	- Sistema de observabilidad completo (RA3)
	"""
	# Generar trace ID único para trazabilidad
	trace_id = logger.generate_trace_id()
	
	# IE6: Validación de seguridad - Rate Limiting
	is_allowed, rate_error = rate_limiter.check_rate_limit(req.session_id)
	if not is_allowed:
		logger.warning('rate_limit_exceeded', {'session_id': req.session_id})
		return ChatResponse(answer=f"⚠️ {rate_error}. Por favor espera un momento.")
	
	# IE6: Validación de seguridad - Prompt Injection
	is_valid, validation_error = SecurityValidator.validate_input(req.question)
	if not is_valid:
		logger.warning('invalid_input_detected', {
			'session_id': req.session_id,
			'error': validation_error
		})
		metrics.track_error('security', 'InvalidInput', validation_error)
		return ChatResponse(answer="⚠️ Por seguridad, no puedo procesar esta consulta.")
	
	# Iniciar tracking de métricas y logging
	start_time = time.time()
	
	# Sanitizar PII de la query antes de loggear
	sanitized_query = SecurityValidator.sanitize_pii(req.question)
	metrics.start_request(trace_id, sanitized_query, req.session_id)
	logger.log_request_start(trace_id, sanitized_query, req.session_id)
	
	try:
		# Usar el agente con memoria y herramientas
		agent_start = time.time()
		answer = agent.think(req.question)
		agent_end = time.time()
		
		# Registrar latencia del agente
		metrics.track_component('agent.think', agent_start, agent_end, {
			'query_length': len(req.question),
			'response_length': len(answer)
		})
		
		# Finalizar tracking exitoso
		end_time = time.time()
		total_latency = end_time - start_time
		metrics.end_request(answer, status="success")
		logger.log_request_end(answer, status="success", latency=total_latency)
		
		# Guardar métricas cada 10 requests
		if len(metrics.metrics_data['requests']) % 10 == 0:
			metrics.save_to_file('backend/logs/metrics.json')
		
		return ChatResponse(answer=answer)
		
	except Exception as e:
		# Registrar error
		end_time = time.time()
		error_msg = str(e)
		
		metrics.track_error('api', type(e).__name__, error_msg)
		metrics.end_request("", status="error")
		logger.error('request_failed', {
			'error_type': type(e).__name__,
			'error_message': error_msg,
			'latency': end_time - start_time
		})
		
		# Guardar métricas en caso de error
		metrics.save_to_file('backend/logs/metrics.json')
		
		return ChatResponse(answer=f"Error en el agente: {error_msg}")


@app.get("/api/metrics")
async def get_metrics_stats():
	"""
	Endpoint para consultar métricas del sistema en tiempo real.
	Usado por el dashboard de Streamlit.
	"""
	try:
		stats = metrics.get_summary_stats()
		return {
			"status": "success",
			"data": stats,
			"timestamp": time.time()
		}
	except Exception as e:
		return {
			"status": "error",
			"error": str(e)
		}


@app.post("/api/plan", response_model=PlanResponse)
async def plan(req: PlanRequest):
	"""
	IE5: Endpoint para planificación de tareas
	
	Crea un plan jerárquico para alcanzar un objetivo.
	"""
	try:
		steps = agent.plan_task(req.objective)
		
		return PlanResponse(plan=steps, objective=req.objective)
	except Exception as e:
		return PlanResponse(plan=[f"Error: {str(e)}"], objective=req.objective)


@app.get("/api/tools")
async def list_tools():
	"""Lista las herramientas disponibles del agente."""
	# Herramientas hardcodeadas para evitar problemas de importación
	tools = [
		{"name": "search_book", "description": "Buscar libros por término"},
		{"name": "check_availability", "description": "Verificar disponibilidad de un libro"},
		{"name": "create_loan", "description": "Crear un préstamo"},
		{"name": "calculate_fine", "description": "Calcular multa por retraso"},
		{"name": "get_policies", "description": "Consultar políticas"},
		{"name": "reserve_book", "description": "Reservar un libro"}
	]
	return {"tools": tools}


@app.get("/api/memory")
async def get_memory():
	"""Consultar el estado de la memoria del agente (IE3)."""
	try:
		history = agent.memory.get_full_history()
		summary = agent.memory.conversation_summary
		user_profile = agent.memory.get_user_profile()  # IE3: Perfil del usuario
		
		return {
			"history_count": len(history),
			"summary": summary,
			"user_profile": user_profile,  # IE3: Información personal del usuario
			"recent_context": agent.memory.get_recent_context(n=3)
		}
	except Exception as e:
		return {"error": str(e)}


@app.delete("/api/memory")
async def clear_memory():
	"""Limpia la memoria del agente."""
	try:
		agent.memory.clear()
		return {"message": "Memoria limpiada exitosamente"}
	except Exception as e:
		return {"error": str(e)}
