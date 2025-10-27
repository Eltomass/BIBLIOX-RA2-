from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from typing import Optional

"""
IL1.3 - Integración LLM + Herramientas de Recuperación
- Cliente de LLM en Ollama y embeddings asociados (con fallback a sentence-transformers).
- La URL base y modelo se heredan del entorno de Ollama del sistema.
"""

OLLAMA_BASE = "http://localhost:11434"


def get_llm(model: str = "llama3.1:8b") -> Ollama:
	return Ollama(model=model, base_url=OLLAMA_BASE)


def get_embeddings(model: str = "nomic-embed-text"):
	# Usa embeddings de Ollama; si falla, cae a sentence-transformers
	try:
		return OllamaEmbeddings(model=model, base_url=OLLAMA_BASE)
	except Exception:
		from langchain_community.embeddings import SentenceTransformerEmbeddings
		return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
