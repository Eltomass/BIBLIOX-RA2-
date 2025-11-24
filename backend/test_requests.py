import requests
import time

API_URL = "http://localhost:8000/api/chat"

queries = [
    "Busca libros de programación",
    "Calcula la multa por 5 días de retraso",
    "Cuántos días puedo tener un libro prestado?",
    "Busca libros de Python",
    "¿Hay libros de García Márquez disponibles?",
    "Dame información sobre renovación de préstamos",
    "Calcula la multa por 10 días",
    "Busca libros de historia",
    "Quiero reservar un libro",
    "Cuáles son las políticas de la biblioteca?"
]

print("Generando requests de prueba...")
print("=" * 50)

for i, query in enumerate(queries, 1):
    print(f"\n[{i}/10] Enviando: {query[:40]}...")
    try:
        response = requests.post(
            API_URL,
            json={"question": query},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            print(f"OK Respuesta: {answer[:80]}...")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(1)

print("\n" + "=" * 50)
print("Generacion de datos completada!")
print("\nAhora abre el dashboard:")
print("   streamlit run streamlit_dashboard.py")
