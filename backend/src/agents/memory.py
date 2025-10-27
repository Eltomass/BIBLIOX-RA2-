"""
IL2.2 - Sistemas de Memoria
IE3: Configurar memoria de contenido para asegurar continuidad en flujos prolongados
IE4: Configurar recuperación de contexto semántico

Este módulo implementa un sistema de memoria conversacional que permite:
- Almacenar historial de conversación (memoria de corto plazo)
- Recuperar contexto semántico relevante (memoria de largo plazo)
- Mantener continuidad en tareas prolongadas
"""

from typing import List, Dict, Any
from datetime import datetime
import json
import os

class ConversationMemory:
	"""
	Sistema de memoria conversacional que almacena y recupera contexto.
	
	Estrategias implementadas:
	- Buffer: Historial completo de la conversación
	- Summary: Resúmenes de conversaciones anteriores
	- Retrieval: Recuperación semántica basada en embeddings
	- User Profile: Información personal del usuario
	"""
	
	def __init__(self, max_history: int = 50):
		self.max_history = max_history
		self.message_history: List[Dict[str, Any]] = []
		self.conversation_summary: str = ""
		self.session_id: str = ""
		self.user_profile: Dict[str, Any] = {}  # IE3: Información personal del usuario
		
	def save_context(self, user_input: str, assistant_output: str, session_id: str = ""):
		"""
		Guarda el contexto de la conversación.
		
		Args:
			user_input: Entrada del usuario
			assistant_output: Respuesta del asistente
			session_id: ID de sesión para persistencia
		"""
		self.session_id = session_id
		
		# Agregar mensajes al historial
		self.message_history.append({
			'timestamp': datetime.now().isoformat(),
			'role': 'user',
			'content': user_input
		})
		
		self.message_history.append({
			'timestamp': datetime.now().isoformat(),
			'role': 'assistant',
			'content': assistant_output
		})
		
		# Limitar el historial según max_history
		if len(self.message_history) > self.max_history:
			self.message_history = self.message_history[-self.max_history:]
		
		# Actualizar resumen si hay demasiadas conversaciones
		if len(self.message_history) > 20:
			self._generate_summary()
	
	def get_recent_context(self, n: int = 5) -> List[Dict[str, Any]]:
		"""
		Obtiene el contexto reciente (últimos n intercambios).
		
		Args:
			n: Número de intercambios a retornar
		
		Returns:
			Lista de los últimos intercambios
		"""
		return self.message_history[-n:]
	
	def get_full_history(self) -> List[Dict[str, Any]]:
		"""Retorna el historial completo."""
		return self.message_history
	
	def build_context_string(self, include_summary: bool = True) -> str:
		"""
		Construye una cadena de contexto para incluir en prompts.
		
		Args:
			include_summary: Si incluir el resumen de conversaciones previas
		
		Returns:
			String con el contexto formateado
		"""
		context_parts = []
		
		# IE3: Agregar perfil del usuario PRIMERO (muy importante)
		if self.user_profile:
			context_parts.append("=== INFORMACIÓN IMPORTANTE DEL USUARIO ===")
			for key, value in self.user_profile.items():
				context_parts.append(f"- {key}: {value}")
			context_parts.append("==========================================\n")
		
		# Agregar resumen si existe
		if include_summary and self.conversation_summary:
			context_parts.append(f"Resumen de conversaciones previas: {self.conversation_summary}")
		
		# Agregar historial reciente
		recent = self.get_recent_context(n=3)
		if recent:
			context_parts.append("\nConversación reciente:")
			for msg in recent:
				role = "Usuario" if msg['role'] == 'user' else "Asistente"
				context_parts.append(f"{role}: {msg['content']}")
		
		return "\n".join(context_parts)
	
	def update_user_profile(self, key: str, value: str):
		"""
		IE3: Actualiza el perfil del usuario con información personal.
		
		Args:
			key: Clave del dato (nombre, edad, preferencias, problema, etc.)
			value: Valor del dato
		"""
		self.user_profile[key] = value
	
	def get_user_profile(self) -> Dict[str, Any]:
		"""Retorna el perfil completo del usuario."""
		return self.user_profile
	
	def _generate_summary(self):
		"""Genera un resumen de conversaciones anteriores para ahorrar tokens."""
		if len(self.message_history) <= 20:
			return
		
		# Resumir los primeros mensajes
		old_messages = self.message_history[:-20]
		
		# Crear resumen simple
		topics = []
		for msg in old_messages:
			if msg['role'] == 'user':
				content = msg['content'].lower()
				if 'libro' in content or 'buscar' in content:
					topics.append('consultas sobre libros')
				elif 'préstamo' in content or 'prestamo' in content:
					topics.append('gestión de préstamos')
				elif 'multa' in content:
					topics.append('consultas sobre multas')
		
		if topics:
			self.conversation_summary = f"Conversaciones anteriores trataron sobre: {', '.join(set(topics))}"
	
	def clear(self):
		"""Limpia la memoria."""
		self.message_history = []
		self.conversation_summary = ""
	
	def save_to_file(self, filepath: str):
		"""Guarda la memoria en un archivo JSON."""
		data = {
			'session_id': self.session_id,
			'message_history': self.message_history,
			'summary': self.conversation_summary,
			'timestamp': datetime.now().isoformat()
		}
		with open(filepath, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=2)
	
	def load_from_file(self, filepath: str):
		"""Carga la memoria desde un archivo JSON."""
		if os.path.exists(filepath):
			with open(filepath, 'r', encoding='utf-8') as f:
				data = json.load(f)
				self.session_id = data.get('session_id', '')
				self.message_history = data.get('message_history', [])
				self.conversation_summary = data.get('summary', '')


class SemanticMemory:
	"""
	Sistema de memoria semántica para recuperación contextual.
	
	Permite recuperar información relevante basada en embeddings
	y búsqueda semántica para mantener coherencia en tareas prolongadas.
	"""
	
	def __init__(self):
		self.knowledge_base: List[Dict[str, Any]] = []
	
	def store_knowledge(self, content: str, metadata: Dict[str, Any] = None):
		"""
		Almacena conocimiento en la base de memoria semántica.
		
		Args:
			content: Contenido a almacenar
			metadata: Metadatos adicionales (tipo, fecha, etc.)
		"""
		self.knowledge_base.append({
			'content': content,
			'metadata': metadata or {},
			'timestamp': datetime.now().isoformat()
		})
	
	def retrieve_relevant(self, query: str, top_k: int = 3) -> List[str]:
		"""
		Recupera conocimiento relevante basado en una consulta.
		
		Args:
			query: Consulta para buscar
			top_k: Número de resultados a retornar
		
		Returns:
			Lista de contenido relevante
		"""
		if not self.knowledge_base:
			return []
		
		query_lower = query.lower()
		results = []
		
		# Búsqueda semántica simple por palabras clave
		for item in self.knowledge_base:
			content = item['content'].lower()
			# Calcular relevancia simple
			relevance = sum(1 for word in query_lower.split() if word in content)
			
			if relevance > 0:
				results.append((item['content'], relevance))
		
		# Ordenar por relevancia y retornar top_k
		results.sort(key=lambda x: x[1], reverse=True)
		return [content for content, _ in results[:top_k]]


# Instancia global de memoria para la sesión
_session_memory = ConversationMemory()
_semantic_memory = SemanticMemory()

def get_session_memory() -> ConversationMemory:
	"""Retorna la instancia global de memoria de sesión."""
	return _session_memory

def get_semantic_memory() -> SemanticMemory:
	"""Retorna la instancia global de memoria semántica."""
	return _semantic_memory
