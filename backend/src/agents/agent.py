"""
IL2.1 e IL2.3 - Arquitectura de Agentes y Planificación
IE2: Integrar frameworks adecuados para el desarrollo del agente
IE5: Diseñar esquemas de planificación de tareas
IE6: Implementar toma de decisiones adaptativas según condiciones del entorno

Este módulo implementa un agente con:
- Patrón ReAct (Razonamiento + Acción)
- Planificación jerárquica de tareas
- Toma de decisiones adaptativa
- Integración con herramientas
"""

import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any, Tuple
from agents.tools import AGENT_TOOLS
from agents.memory import get_session_memory, get_semantic_memory
from models.llm import get_llm


class LibraryAgent:
	"""
	Agente inteligente para gestión de biblioteca con capacidad de:
	- Razonamiento y planificación
	- Uso de herramientas
	- Memoria conversacional
	- Toma de decisiones adaptativa
	"""
	
	def __init__(self):
		self.llm = get_llm()
		self.tools = {tool['name']: tool['func'] for tool in AGENT_TOOLS}
		self.memory = get_session_memory()
		self.semantic_memory = get_semantic_memory()
		self.plan = []
		self.max_iterations = 5
	
	def think(self, question: str) -> str:
		"""
		IE3, IE4, IE6: Memoria, Contexto y Toma de decisiones adaptativas
		
		Permite al agente razonar sobre la pregunta y decidir:
		1. Qué herramientas necesita usar
		2. En qué orden ejecutarlas
		3. Cómo adaptarse a las respuestas de las herramientas
		
		Args:
			question: Pregunta del usuario
		
		Returns:
			Respuesta final del agente
		"""
		# Construir contexto con memoria (IE3, IE4)
		context = self.memory.build_context_string()
		
		# Prompt con patrón ReAct mejorado para memoria
		system_prompt = """Eres BiblioAgent, un asistente inteligente de biblioteca con memoria conversacional.

IMPORTANTE: 
- Debes RECORDAR información personal del usuario como nombre, edad, preferencias, problemas que te haya contado, etc.
- Si el usuario menciona datos personales (nombre, edad, problemas, intereses), GUÁRDALOS en tu memoria para referencias futuras
- Usa esta información en tus respuestas para personalizar la experiencia

Tu tarea es:
1. Extraer información personal del usuario de sus mensajes
2. Analizar la pregunta del usuario
3. Decidir qué herramientas necesitas usar
4. Ejecutar las herramientas necesarias
5. Responder de manera clara, útil y PERSONALIZADA usando la información que recuerdes del usuario

Herramientas disponibles:
- search_book(termino): Buscar libros
- check_availability(titulo): Verificar disponibilidad
- create_loan(user_id, titulo): Crear préstamo
- calculate_fine(dias): Calcular multa
- get_policies(consulta): Consultar políticas
- reserve_book(user_id, titulo): Reservar libro

Formato de razonamiento:
Thought: [tu razonamiento sobre qué hacer]
Action: [nombre_herramienta]
Action Input: [parámetros]
Observation: [resultado de la acción]
... (repetir si es necesario)
Final Answer: [respuesta final al usuario]

Si no necesitas herramientas, responde directamente."""
		
		user_prompt = f"""Contexto de conversaciones anteriores:
{context if context else "Primera conversación - no hay contexto previo"}

Pregunta del usuario: {question}

Responde siguiendo el patrón ReAct y RECUERDA información importante del usuario."""
		
		# Ejecutar el LLM con ReAct
		response = self._execute_react(f"{system_prompt}\n\n{user_prompt}")
		
		# Extraer la respuesta final (sin Thought/Action/Observation)
		final_answer = self._extract_final_answer(response)
		
		# IE3: Extraer información personal del usuario de la conversación
		self._extract_user_info(question)
		
		# Guardar en memoria (IE3)
		self.memory.save_context(question, final_answer)
		
		return final_answer
	
	def _extract_user_info(self, user_message: str):
		"""
		IE3: Extrae información personal del usuario de sus mensajes.
		
		Detecta y almacena:
		- Nombre
		- Edad
		- Preferencias
		- Problemas
		- Cualquier información personal relevante
		"""
		import re
		
		# Patrones para detectar información personal
		name_patterns = [
			r'(?:me llamo|mi nombre es|soy|me llaman)\s+([A-Z][a-z]+)',
			r'nombre\s+([A-Z][a-z]+)',
			r'yo\s+([A-Z][a-z]+)\s+(?:y|tengo|trabajo)',
		]
		
		age_patterns = [
			r'(?:tengo|tengo edad de|edad de)\s+(\d+)\s+(?:años|years)',
			r'(?:años|age)\s+(?:de|:)\s*(\d+)',
		]
		
		problem_patterns = [
			r'(?:problema es|tengo|mi problema|una dificultad)',
		]
		
		# Extraer nombre
		for pattern in name_patterns:
			match = re.search(pattern, user_message, re.IGNORECASE)
			if match:
				name = match.group(1)
				# Verificar que no sea una palabra común
				if name.lower() not in ['yo', 'me', 'te', 'el', 'lo', 'la', 'le', 'nos', 'les']:
					self.memory.update_user_profile('nombre', name)
					break
		
		# Extraer edad
		for pattern in age_patterns:
			match = re.search(pattern, user_message, re.IGNORECASE)
			if match:
				age = match.group(1)
				self.memory.update_user_profile('edad', age)
				break
		
		# Extraer si menciona un problema o dificultad
		if re.search(problem_patterns[0], user_message, re.IGNORECASE):
			# Intentar extraer la descripción del problema
			problem_text = user_message
			# Guardar el contexto del problema
			self.memory.update_user_profile('problema_actual', problem_text[:200])  # Primeros 200 caracteres
		
		# Detectar preferencias de libros
		if any(word in user_message.lower() for word in ['me gusta', 'prefiero', 'me interesa', 'me encanta']):
			# Extraer el tema de interés
			for word in ['ficcion', 'ciencia', 'historia', 'programacion', 'novelas', 'poesia', 'filosofia']:
				if word in user_message.lower():
					self.memory.update_user_profile('preferencia_genero', word)
					break
	
	def _extract_final_answer(self, response: str) -> str:
		"""
		Extrae la respuesta final del patrón ReAct.
		"""
		# Buscar "Final Answer:" y extraer lo que sigue
		if "Final Answer:" in response:
			return response.split("Final Answer:")[-1].strip()
		
		# Si no hay "Final Answer:", tomar la última línea
		lines = response.split('\n')
		# Filtrar líneas que no son parte de ReAct
		clean_lines = []
		for line in lines:
			if line.strip() and not any(line.strip().startswith(x) for x in ["Thought:", "Action:", "Action Input:", "Observation:"]):
				clean_lines.append(line.strip())
		
		return '\n'.join(clean_lines) if clean_lines else response
	
	def _execute_react(self, prompt: str) -> str:
		"""
		Ejecuta el patrón ReAct iterativamente.
		
		Args:
			prompt: Prompt inicial
		
		Returns:
			Respuesta final del agente
		"""
		current_prompt = prompt
		
		for iteration in range(self.max_iterations):
			# Obtener respuesta del LLM
			llm_response = self.llm.invoke(current_prompt)
			
			# Verificar si hay acciones que ejecutar
			action = self._parse_action(llm_response)
			
			if not action or "Final Answer" in llm_response:
				# Extraer respuesta final
				if "Final Answer:" in llm_response:
					return llm_response.split("Final Answer:")[-1].strip()
				return llm_response
			
			# Ejecutar acción
			action_result = self._execute_action(action)
			
			# Actualizar prompt con observación
			current_prompt += f"\n\nObservation: {action_result}"
			
			# Solicitar siguiente pensamiento
			current_prompt += "\n\nPensemos en el siguiente paso basándonos en esta observación."
		
		# Si llegamos aquí, retornar última respuesta
		return llm_response
	
	def _parse_action(self, response: str) -> Dict[str, Any]:
		"""
		Extrae acción de la respuesta del LLM.
		
		Args:
			response: Respuesta del LLM
		
		Returns:
			Dict con 'tool' y 'input' o None
		"""
		# Buscar patrón "Action: tool_name"
		action_match = re.search(r'Action:\s*(\w+)', response)
		if not action_match:
			return None
		
		tool_name = action_match.group(1)
		
		# Buscar input
		input_match = re.search(r'Action Input:\s*(.+)', response)
		action_input = input_match.group(1).strip() if input_match else ""
		
		return {
			'tool': tool_name,
			'input': action_input
		}
	
	def _execute_action(self, action: Dict[str, Any]) -> str:
		"""
		Ejecuta una acción usando las herramientas disponibles.
		
		Args:
			action: Dict con 'tool' (nombre) y 'input' (parámetros)
		
		Returns:
			Resultado de la acción
		"""
		tool_name = action['tool']
		tool_input = action['input']
		
		if tool_name not in self.tools:
			return f"No se encontró la herramienta '{tool_name}'"
		
		# Parsear input (simple para demo)
		try:
			# Ejecutar herramienta con input parseado
			result = self._call_tool(tool_name, tool_input)
			return result
		except Exception as e:
			return f"Error al ejecutar {tool_name}: {str(e)}"
	
	def _call_tool(self, tool_name: str, tool_input: str) -> str:
		"""
		Llama a una herramienta con input parseado.
		
		Args:
			tool_name: Nombre de la herramienta
			tool_input: Input en formato string
		
		Returns:
			Resultado de la herramienta
		"""
		tool_func = self.tools[tool_name]
		
		# Parsear input simple
		inputs = [s.strip() for s in tool_input.split(',')]
		
		# Llamar a la herramienta
		if len(inputs) == 1:
			return tool_func(inputs[0])
		elif len(inputs) == 2:
			return tool_func(inputs[0], inputs[1])
		elif len(inputs) == 3:
			return tool_func(inputs[0], inputs[1], int(inputs[2]) if inputs[2].isdigit() else inputs[2])
		else:
			return tool_func(*inputs)
	
	def plan_task(self, objective: str) -> List[str]:
		"""
		IE5: Planificación de tareas
		
		Crea un plan jerárquico para alcanzar un objetivo.
		
		Args:
			objective: Objetivo a alcanzar
		
		Returns:
			Lista de pasos del plan
		"""
		plan_prompt = f"""Objetivo: {objective}

Desglosa este objetivo en pasos específicos y ordenados.
Cada paso debe ser una acción concreta.
Formato: lista numerada."""
		
		response = self.llm.invoke(plan_prompt)
		
		# Extraer pasos de la lista
		steps = []
		lines = response.split('\n')
		for line in lines:
			# Buscar líneas con números o viñetas
			if re.match(r'^\d+[\.\)]\s+', line) or line.strip().startswith('-'):
				steps.append(line.strip())
		
		self.plan = steps
		return steps
	
	def execute_plan(self, objective: str) -> str:
		"""
		Ejecuta un plan completo para alcanzar un objetivo.
		
		Args:
			objective: Objetivo a alcanzar
		
		Returns:
			Resultado final de la ejecución del plan
		"""
		# Crear plan
		steps = self.plan_task(objective)
		
		results = []
		for i, step in enumerate(steps):
			# Simular ejecución de cada paso
			results.append(f"Paso {i+1}: {step}")
		
		return "\n".join(results)


def get_agent() -> LibraryAgent:
	"""Retorna la instancia global del agente."""
	return LibraryAgent()
