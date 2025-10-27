from typing import List, Tuple
from langchain_community.vectorstores import Chroma

"""
IL1.3 - Arquitectura de Solución Integrada
- Recuperación semántica y ranking por score (menor distancia = más relevante)
  para seleccionar el contexto a inyectar en el prompt de generación.
"""

def retrieve_relevant(vs: Chroma, query: str, k: int = 4) -> List[Tuple[str, float]]:
	"""Retorna lista de (texto, score) ordenada por relevancia ascendente."""
	results = vs.similarity_search_with_score(query, k=k)
	results.sort(key=lambda x: x[1])
	return [(doc.page_content, score) for doc, score in results]
