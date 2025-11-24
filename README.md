│                      FRONTEND (React)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Chat UI    │  │  Components  │  │    Pages    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼─────────────────┼──────────────────┼──────────────┘
          │                 │                  │
          └─────────────────┴──────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              Endpoints:                              │ │
│  │  - POST /api/chat      (Chat con agente)            │ │
│  │  - POST /api/plan      (Planificación de tareas)    │ │
│  │  - GET  /api/tools    (Listar herramientas)         │ │
│  │  - GET  /api/memory   (Consultar memoria)           │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   LIBRARY AGENT (LangChain)                 │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │  Patrón ReAct    │  │   Planificación  │              │
│  │  (Razonamiento   │  │   Jerárquica     │              │
│  │   + Acción)      │  │                  │              │
│  └────────┬─────────┘  └────────┬─────────┘              │
│           │                     │                          │
└───────────┼─────────────────────┼──────────────────────────┘
            │                     │
            ▼                     ▼
┌──────────────────┐   ┌──────────────────┐   ┌────────────┐
│   MEMORIA        │   │   HERRAMIENTAS   │   │    LLM     │
│  Conversacional  │   │                  │   │  (Ollama)  │
│  - Historial     │   │  1. search_book  │   │            │
│  - Resúmenes     │   │  2. check_avail  │   │  qwen2.5   │
│  - Contexto      │   │  3. create_loan  │   │  -coder:7b │
└──────────────────┘   │  4. calc_fine    │   └────────────┘
                       │  5. get_policies │
                       │  6. reserve_book │
                       └──────────────────┘
```

## Estructura del Proyecto

```
IngDeSolucionesIA-BiblioX/
├── src/                          # Frontend React
│   ├── components/               # Componentes reutilizables
│   │   ├── chat/                 # Interfaz de chat
│   │   └── books/                # Gestión de libros
│   ├── pages/                    # Páginas principales
│   ├── hooks/                     # Custom hooks
│   └── services/                  # Servicios de API
├── backend/                       # Backend Python
│   ├── src/
│   │   ├── api.py                 # API principal con agente
│   │   ├── agents/                 # 🆕 Sistema de Agentes
│   │   │   ├── agent.py            # Agente principal (ReAct)
│   │   │   ├── tools.py            # Herramientas del agente
│   │   │   ├── memory.py           # Sistema de memoria
│   │   │   └── router.py          # Router de dominios
│   │   ├── models/                 # Modelos de IA
│   │   ├── rag/                    # Sistema RAG
│   │   └── data/                   # Datos de la biblioteca
│   └── requirements.txt
├── public/                         # Archivos estáticos
└── README.md                       # Este archivo
```

## 🛠️ Tecnologías Utilizadas

### Frontend
- **React 19**: Framework UI moderno
- **Tailwind CSS**: Estilos utilitarios
- **React Router**: Navegación

### Backend
- **Python 3.12**: Lenguaje principal
- **FastAPI**: Framework web asíncrono
- **LangChain 1.0**: Framework de agentes IA
- **Ollama**: Runtime local para LLMs
- **Uvicorn**: Servidor ASGI

### IA y Agent Frameworks
- **qwen2.5-coder:7b**: Modelo LLM para razonamiento
- **nomic-embed-text**: Modelo de embeddings para recuperación semántica
- **Patrón ReAct**: Razonamiento + Acción para agentes autónomos

## ✅ Capacidades del Sistema

Este sistema demuestra las siguientes capacidades:

1. **Herramientas Autónomas**: El agente ejecuta automáticamente búsquedas, préstamos, cálculos de multas y consultas de políticas
2. **Memoria Conversacional**: Recuerda tu nombre, edad, preferencias y problemas que le compartes durante toda la sesión
3. **Planificación de Tareas**: Descompone objetivos complejos en pasos ejecutables
4. **Toma de Decisiones Adaptativa**: Ajusta su comportamiento según el contexto y respuestas inesperadas
5. **Recuperación de Contexto**: Mantiene coherencia en conversaciones prolongadas
6. **Integración con Ollama**: Usa modelos locales de IA sin necesidad de API externas
7. **Arquitectura Modular**: Código organizado en agentes, herramientas, memoria y planificación
8. **API Documentada**: Endpoints REST para chat, planificación, herramientas y memoria

---

## 🔧 Herramientas del Agente

El agente implementa 6 herramientas especializadas para operaciones autónomas:

| Herramienta | Función | Ejemplo |
|------------|---------|---------|
| `search_book` | Buscar libros por término | `search_book("código")` |
| `check_availability` | Verificar disponibilidad | `check_availability("Python for Data")` |
| `create_loan` | Crear préstamo | `create_loan("user123", "Libro", 14)` |
| `calculate_fine` | Calcular multa | `calculate_fine(5)` |
| `get_policies` | Consultar políticas | `get_policies("renovación")` |
| `reserve_book` | Reservar libro | `reserve_book("user123", "Libro")` |

**Justificación**: Se implementaron estas 6 herramientas porque cubren el flujo completo de operaciones bibliotecarias: búsqueda → verificación → préstamo → gestión de multas → políticas → reservas. Cada herramienta es independiente y autónoma, permitiendo al agente ejecutar funciones específicas sin intervención manual.

---

## 🧠 Sistema de Memoria

### Memoria Conversacional
- **Historial de conversación**: Almacena todos los mensajes
- **Perfil de usuario**: Recuerda nombre, edad, preferencias y problemas
- **Resúmenes automáticos**: Genera resúmenes para conversaciones largas (50+ mensajes)
- **Límite inteligente**: Mantiene solo lo más relevante para eficiencia

### Recuperación Contextual
- **Búsqueda semántica**: Encuentra información relevante por significado
- **Persistencia**: Los datos se mantienen durante la sesión
- **Contexto completo**: Incluye información personal en cada respuesta

**Cómo funciona**: El sistema almacena automáticamente:
- Tu nombre cuando te presentas
- Tu edad si la mencionas
- Problemas o dificultades que compartes
- Preferencias de lectura o intereses

---

## 📋 Planificación de Tareas

El agente implementa planificación jerárquica mediante:
- Método `plan_task(objective)`: Descompone objetivos complejos en pasos
- Método `execute_plan()`: Ejecuta planes multi-paso
- Iteraciones adaptativas con `max_iterations = 5`

**Ejemplo de Planificación**:
```
Objetivo: "Prestar un libro de Python a un usuario"

Plan generado:
1. Buscar libro "Python"
2. Verificar disponibilidad
3. Crear préstamo
4. Confirmar con usuario
```

**Justificación**: La planificación jerárquica permite al agente manejar objetivos complejos descomponiéndolos en tareas ejecutables, similar a la planificación automática en sistemas de agentes reales.

---

## 🎯 Toma de Decisiones Adaptativa

El agente utiliza el **patrón ReAct** (Razonamiento + Acción):

1. **Thought**: El agente razona sobre qué hacer
2. **Action**: Decide qué herramienta usar
3. **Observation**: Observa el resultado
4. **Final Answer**: Responde al usuario

**Ejemplo de Flujo**:
```
Usuario: "¿Hay libros de programación disponibles?"

Thought: Necesito buscar libros de programación
Action: search_book
Input: "programación"
Observation: Encontré 5 libros...
Final Answer: Sí, encontré estos libros...
```

**Justificación**: El patrón ReAct permite al agente adaptarse a respuestas imprevistas y tomar nuevas acciones basadas en observaciones, demostrando comportamiento adaptativo real.

---

## 🎓 Justificación de Componentes

### ¿Por qué estas tecnologías?

### Framework: LangChain
**¿Por qué LangChain?**
- **Integración nativa** con Ollama (modelos locales)
- **Abstracciones de alto nivel** para agentes
- **Soporte para herramientas** (function calling)
- **Ecosistema maduro** con comunidades activas
- **Compatibilidad** con modelos locales como qwen2.5-coder

### Modelo: qwen2.5-coder:7b
**¿Por qué este modelo?**
- **Óptimo para código**: Diseñado para razonamiento técnico
- **Modo local**: No requiere API keys ni costos
- **Tamaño moderado**: 7B parámetros balancean calidad/velocidad
- **Licencia permisiva**: Comercialmente usable
- **Dispuesto en la máquina**: Ya instalado

### Arquitectura: ReAct + Memoria
**¿Por qué ReAct?**
- **Transparencia**: El agente explica su razonamiento
- **Debuggeable**: Fácil ver errores en la cadena
- **Iterativo**: Permite corregir acciones anteriores
- `npm run build`: Construye la aplicación para producción

### Backend
- `python src/api.py`: Inicia el servidor API
- `streamlit run streamlit_app.py`: Inicia la interfaz Streamlit

## Funcionalidades

- **Catálogo de Libros**: Búsqueda y filtrado avanzado
- **Sistema de Préstamos**: Gestión completa de préstamos y devoluciones
- **Chat Inteligente**: Asistente de IA para consultas sobre la biblioteca
- **Gestión de Usuarios**: Perfiles y historial de transacciones
- **Sistema de Multas**: Cálculo automático de multas por retrasos

## Documentación

El proyecto incluye documentación adicional en los archivos:
- `Informe de Propuesta de Solución con IA para BiblioX.docx`
- `Informe-de-Propuesta-de-Solucion-con-IA-para-LibreriaX.pptx`

## Contribución

Este proyecto forma parte de una evaluación académica en Ingeniería Informática.