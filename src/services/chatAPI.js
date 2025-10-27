/**
 * Servicio de chat del frontend.
 * Encapsula las llamadas HTTP al backend FastAPI para enviar preguntas
 * al asistente y recibir respuestas.
 */
const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

/**
 * Envía una pregunta al asistente del backend y retorna el texto de respuesta.
 * @param {string} question - Texto ingresado por el usuario.
 * @returns {Promise<string>} - Respuesta del asistente.
 */
export async function askAssistant(question) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error('Error en el backend');
  const data = await res.json();
  return data.answer;
}
