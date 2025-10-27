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

# Importar el agente y sus dependencias
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents.agent import get_agent

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
	"""
	try:
		# Usar el agente con memoria y herramientas
		answer = agent.think(req.question)
		
		return ChatResponse(answer=answer)
	except Exception as e:
		return ChatResponse(answer=f"Error en el agente: {str(e)}")


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
