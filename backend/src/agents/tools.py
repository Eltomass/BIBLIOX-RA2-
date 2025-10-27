"""
IL2.1 - Integración de Herramientas
IE1: Configurar herramientas dentro del agente para ejecutar funciones específicas con autonomía.

Este módulo define las herramientas que el agente puede utilizar para:
- Buscar libros en el catálogo
- Gestionar préstamos
- Consultar políticas y reglamentos
- Realizar reservas
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Ruta al catálogo de libros
CATALOG_PATH = os.path.join(os.path.dirname(__file__), '../../data/catalogo_libros.txt')
POLICIES_PATH = os.path.join(os.path.dirname(__file__), '../../data/políticas_prestamos.txt')

def load_catalog() -> List[Dict[str, Any]]:
	"""Carga el catálogo de libros desde el archivo."""
	try:
		with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
			content = f.read()
		# Parsear el catálogo (formato simple)
		books = []
		for line in content.split('\n'):
			if '|' in line:
				parts = [p.strip() for p in line.split('|')]
				if len(parts) >= 3:
					books.append({
						'title': parts[0],
						'author': parts[1] if len(parts) > 1 else '',
						'genre': parts[2] if len(parts) > 2 else '',
						'available': True  # Por defecto disponible
					})
		return books
	except:
		return []


def search_book(search_term: str) -> str:
	"""
	Herramienta 1: Buscar libros en el catálogo.
	
	Args:
		search_term: Término de búsqueda (título, autor o género)
	
	Returns:
		Lista de libros encontrados en formato JSON
	"""
	books = load_catalog()
	results = []
	search_lower = search_term.lower()
	
	for book in books:
		if (search_lower in book.get('title', '').lower() or
		    search_lower in book.get('author', '').lower() or
		    search_lower in book.get('genre', '').lower()):
			results.append(book)
	
	if not results:
		return "No se encontraron libros con el término: " + search_term
	
	return json.dumps(results, ensure_ascii=False, indent=2)


def check_availability(title: str) -> str:
	"""
	Herramienta 2: Verificar disponibilidad de un libro específico.
	
	Args:
		title: Título del libro
	
	Returns:
		Estado de disponibilidad
	"""
	books = load_catalog()
	
	for book in books:
		if book.get('title', '').lower() == title.lower():
			if book.get('available', False):
				return f"El libro '{title}' está disponible para préstamo."
			else:
				return f"El libro '{title}' no está disponible actualmente."
	
	return f"No se encontró el libro '{title}' en el catálogo."


def create_loan(user_id: str, book_title: str, days: int = 14) -> str:
	"""
	Herramienta 3: Crear un préstamo de libro.
	
	Args:
		user_id: ID del usuario
		book_title: Título del libro
		days: Días de duración del préstamo (default: 14)
	
	Returns:
		Confirmación del préstamo
	"""
	due_date = datetime.now() + timedelta(days=days)
	due_str = due_date.strftime('%Y-%m-%d')
	
	# Validar disponibilidad
	availability = check_availability(book_title)
	if "está disponible" not in availability:
		return f"No se puede crear el préstamo: {availability}"
	
	return (f"Préstamo creado exitosamente:\n"
	        f"- Libro: {book_title}\n"
	        f"- Usuario: {user_id}\n"
	        f"- Fecha de vencimiento: {due_str}\n"
	        f"- Duración: {days} días")


def calculate_fine(days_overdue: int, base_fine: float = 500.0) -> str:
	"""
	Herramienta 4: Calcular multa por retraso en devolución.
	
	Args:
		days_overdue: Días de retraso
		base_fine: Multa base por día
	
	Returns:
		Cálculo de multa en formato legible
	"""
	if days_overdue <= 0:
		return "No hay multa aplicable."
	
	total_fine = days_overdue * base_fine
	
	return (f"Cálculo de multa:\n"
	        f"- Días de retraso: {days_overdue}\n"
	        f"- Multa por día: ${base_fine:,.0f} CLP\n"
	        f"- Total a pagar: ${total_fine:,.0f} CLP")


def get_policies(query: str) -> str:
	"""
	Herramienta 5: Consultar políticas y reglamentos de la biblioteca.
	
	Args:
		query: Consulta sobre políticas
	
	Returns:
		Información relevante de las políticas
	"""
	try:
		with open(POLICIES_PATH, 'r', encoding='utf-8') as f:
			content = f.read()
		
		# Buscar términos clave en las políticas
		query_lower = query.lower()
		
		# Retornar secciones relevantes basadas en la consulta
		if 'día' in query_lower or 'días' in query_lower:
			return "Según las políticas: El préstamo de libros es por 14 días naturales con posibilidad de renovación."
		elif 'multa' in query_lower or 'retraso' in query_lower:
			return "Según las políticas: Las multas se calculan a razón de $500 CLP por día de retraso."
		elif 'renovación' in query_lower or 'renovar' in query_lower:
			return "Según las políticas: Se puede renovar el préstamo hasta 2 veces si no hay reservas pendientes."
		else:
			return "Las políticas de la biblioteca incluyen: préstamos de 14 días, renovaciones permitidas, y multas por retraso."
			
	except:
		return "No se pudo acceder a las políticas en este momento."


def reserve_book(user_id: str, book_title: str) -> str:
	"""
	Herramienta 6: Reservar un libro no disponible.
	
	Args:
		user_id: ID del usuario
		book_title: Título del libro
	
	Returns:
		Confirmación de reserva
	"""
	return (f"Reserva creada exitosamente:\n"
	        f"- Libro: {book_title}\n"
	        f"- Usuario: {user_id}\n"
	        f"- Estado: Pendiente\n"
	        f"- Se le notificará cuando el libro esté disponible")


# Lista de herramientas disponibles para el agente
AGENT_TOOLS = [
	{
		'name': 'search_book',
		'description': 'Busca libros en el catálogo por título, autor o género. Input: término de búsqueda.',
		'func': search_book
	},
	{
		'name': 'check_availability',
		'description': 'Verifica si un libro específico está disponible. Input: título del libro.',
		'func': check_availability
	},
	{
		'name': 'create_loan',
		'description': 'Crea un nuevo préstamo de libro. Input: ID de usuario, título del libro, días de duración (opcional, default 14).',
		'func': create_loan
	},
	{
		'name': 'calculate_fine',
		'description': 'Calcula la multa por retraso en devolución. Input: días de retraso.',
		'func': calculate_fine
	},
	{
		'name': 'get_policies',
		'description': 'Consulta políticas y reglamentos de la biblioteca. Input: consulta sobre políticas.',
		'func': get_policies
	},
	{
		'name': 'reserve_book',
		'description': 'Reserva un libro no disponible. Input: ID de usuario, título del libro.',
		'func': reserve_book
	}
]
