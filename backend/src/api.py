from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

# Base de Ollama y modelo LLM a utilizar. No se fija ruta de modelos aquí;
# se asume configuración por defecto de Ollama o variable de entorno del sistema.
OLLAMA_URL = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")

app = FastAPI()

# CORS abierto para permitir pruebas desde CRA en localhost
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

class ChatRequest(BaseModel):
	"""Payload de entrada del endpoint de chat."""
	question: str

class ChatResponse(BaseModel):
	"""Respuesta con el texto del asistente."""
	answer: str


def ollama_generate(prompt: str) -> str:
	"""Llama a Ollama /api/generate para obtener una respuesta determinística (sin streaming)."""
	resp = requests.post(f"{OLLAMA_URL}/api/generate", json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=120)
	resp.raise_for_status()
	data = resp.json()
	return data.get("response", "")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
	"""Endpoint mínimo de chat: construye un prompt simple y consulta al modelo en Ollama."""
	prompt = (
		"Eres BiblioAssist, asistente experto de biblioteca. Responde en español con precisión y brevedad.\n"
		f"Pregunta: {req.question}\n"
		"Respuesta:"
	)
	try:
		answer = ollama_generate(prompt)
	except Exception as e:
		# Respuesta controlada en caso de que Ollama no esté disponible
		answer = f"No pude contactar al modelo en Ollama ({e})."
	return ChatResponse(answer=answer)
