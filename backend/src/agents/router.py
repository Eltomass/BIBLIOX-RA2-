"""
IL1.3 - Arquitectura Integrada
- Router simple para decidir el dominio de la consulta y elegir prompts/recuperación adecuados.
"""

def detect_domain(question: str) -> str:
	q = question.lower()
	policy_keywords = ["multa", "préstamo", "prestamo", "renovación", "renovar", "período", "reservas", "límite"]
	for kw in policy_keywords:
		if kw in q:
			return 'policies'
	return 'books'
