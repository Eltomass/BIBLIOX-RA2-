from .prompts import POLICIES_SYSTEM, POLICIES_USER_TEMPLATE, BOOKS_SYSTEM, BOOKS_USER_TEMPLATE
from ...models.llm import get_llm

"""
IL1.1 - Formulación de Prompts Optimizados
- Definición de prompts diferenciados para dominio de políticas y de libros.

IL1.3 - Arquitectura de Solución Integrada
- Integración LLM (Ollama) + recuperación (inyectada vía "context")
  para controlar el tamaño de contexto y priorizar información relevante
  antes de invocar el modelo.
"""

def generate_answer(question: str, context: str, domain: str = 'policies') -> str:
	# Selección del sistema y plantilla según dominio (políticas/libros)
	llm = get_llm()
	if domain == 'policies':
		prompt = f"<system>{POLICIES_SYSTEM}</system>\n" + POLICIES_USER_TEMPLATE.format(context=context, question=question)
	else:
		prompt = f"<system>{BOOKS_SYSTEM}</system>\n" + BOOKS_USER_TEMPLATE.format(context=context, question=question)
	# Invocación al LLM con el prompt construido
	return llm.invoke(prompt)
