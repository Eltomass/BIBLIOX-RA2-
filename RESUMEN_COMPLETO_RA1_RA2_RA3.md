# Resumen Completo: Ingeniería de Soluciones con Inteligencia Artificial

## 📖 Descripción General del Curso

Este curso cubre desde los fundamentos de la IA generativa y el prompt engineering, hasta el desarrollo de agentes inteligentes y las mejores prácticas para llevar soluciones a producción, incluyendo observabilidad, seguridad y ética.

**Información General:**
- **Nivel:** Intermedio
- **Modalidad:** Práctica y conceptual  
- **Requisitos:** Python básico, interés en IA
- **Estructura:** 3 Resultados de Aprendizaje (RA), cada uno con 4 Itinerarios de Lecciones (IL)

---

## 🎯 RA1: Fundamentos de IA Generativa y Prompt Engineering

### Descripción General
En la primera experiencia de aprendizaje, los estudiantes desarrollan competencias fundamentales en inteligencia artificial generativa y técnicas de prompt engineering. Se enfatiza la comprensión de modelos de lenguaje (LLMs), sus capacidades, limitaciones y aplicaciones en contextos organizacionales.

### Objetivos Principales
- Comprender arquitecturas y funcionamiento de LLMs
- Trabajar con APIs de modelos de lenguaje
- Explorar técnicas de redacción de prompts efectivos (zero-shot, few-shot, chain-of-thought)
- Implementar infraestructura RAG (Retrieval-Augmented Generation)
- Evaluar y optimizar sistemas LLM

### Evaluaciones RA1
- **Ev For 1**: Quiz Fundamentos IA Generativa (8 preguntas)
- **EV Parcial 1**: Diseño de Solución con LLM y RAG

---

## 📚 IL1.1: Introducción a LLMs y Conexiones API

### Descripción
Esta unidad introduce los conceptos fundamentales de los Modelos de Lenguaje Grandes (LLMs) y las técnicas para establecer conexiones API efectivas.

### Objetivos de Aprendizaje
1. **Comprender los fundamentos de los LLMs**: Arquitectura, funcionamiento y capacidades
2. **Establecer conexiones API**: Configurar y usar APIs de diferentes proveedores
3. **Implementar patrones básicos**: Llamadas síncronas, streaming y gestión de memoria
4. **Aplicar mejores prácticas**: Configuración segura, manejo de errores y optimización

### Contenido del Módulo

#### Notebook 1: Conexión Directa con GitHub Models API
- **Archivo**: `1-github_model_api.ipynb`
- **Qué aprenderás**:
  - Configurar variables de entorno y cliente de `openai`
  - Realizar llamadas básicas `chat.completions.create`
  - Usar parámetros clave: `model`, `messages`, `temperature`, `max_tokens`
  - Aplicar el rol `system` para guiar el comportamiento del modelo

#### Notebook 2: Abstracción con LangChain
- **Archivo**: `2-langchain_model_api.ipynb`
- **Qué aprenderás**:
  - Ventajas de usar LangChain como framework
  - Configurar el objeto `ChatOpenAI`
  - Utilizar el método `invoke` para interactuar
  - Estructura de mensajes: `HumanMessage`, `AIMessage`, `SystemMessage`

#### Notebook 3: Streaming en Tiempo Real
- **Archivo**: `3-langchain_streaming.ipynb`
- **Qué aprenderás**:
  - Qué es el streaming y su importancia para UX
  - Implementar streaming usando `.stream()`
  - Procesar chunks de datos en tiempo real
  - Construir un chatbot fluido

#### Notebook 4: Gestión de Memoria
- **Archivo**: `4-langchain_memory.ipynb`
- **Qué aprenderás**:
  - Importancia de la memoria para conversaciones coherentes
  - Estrategias de memoria:
    - `ConversationBufferMemory`: Guarda todo el historial
    - `ConversationBufferWindowMemory`: Guarda las últimas k interacciones
    - `ConversationSummaryMemory`: Resume la conversación para ahorrar tokens
  - Integrar memoria en cadenas de conversación (`ConversationChain`)

### Configuración del Entorno

**Variables de Entorno Requeridas:**
```bash
export GITHUB_BASE_URL="https://models.inference.ai.azure.com"
export GITHUB_TOKEN="tu_token_de_github"
export OPENAI_BASE_URL="https://models.inference.ai.azure.com"
```

**Dependencias:**
```bash
pip install openai langchain langchain-openai
```

### Consideraciones Técnicas

**Seguridad:**
- Nunca hardcodear API keys en el código
- Usar variables de entorno para credenciales
- Implementar rate limiting y error handling

**Performance:**
- Configurar timeouts apropiados
- Usar streaming para respuestas largas
- Optimizar el uso de tokens

**Escalabilidad:**
- Considerar patrones de retry y circuit breaker
- Implementar logging para debugging
- Planificar para múltiples proveedores

---

## 🎨 IL1.2: Técnicas Avanzadas de Prompt Engineering

### Descripción
Esta unidad profundiza en las técnicas avanzadas de ingeniería de prompts que permiten maximizar el rendimiento de los LLMs en diferentes tipos de tareas.

### Objetivos de Aprendizaje
1. **Aplicar técnicas zero-shot**: Obtener resultados sin ejemplos previos
2. **Implementar few-shot learning**: Usar ejemplos para guiar el comportamiento
3. **Dominar chain-of-thought**: Prompts que fomentan razonamiento paso a paso
4. **Diseñar prompts especializados**: Para diferentes dominios y casos de uso
5. **Evaluar y optimizar prompts**: Métricas y técnicas de mejora iterativa

### Técnicas Core

#### 1. Zero-Shot Prompting
- **Archivo**: `1-zero-shot-prompting.ipynb`
- Prompts sin ejemplos previos
- Instrucciones claras y específicas
- Roles y contexto efectivos
- Casos de uso y limitaciones

#### 2. Few-Shot Prompting
- **Archivo**: `2-few-shot-prompting.ipynb`
- Selección de ejemplos representativos
- Formatos de entrada-salida
- Balanceo de ejemplos
- Optimización del número de shots

#### 3. Chain-of-Thought (CoT)
- **Archivo**: `3-chain-of-thought.ipynb`
- Razonamiento paso a paso
- CoT con y sin ejemplos
- Prompts que fomentan explicaciones
- Aplicaciones en resolución de problemas

#### 4. Técnicas Avanzadas
- **Archivo**: `4-advanced-techniques.ipynb`
- Tree of Thoughts (ToT)
- Self-consistency prompting
- Program-aided language models
- Meta-prompting y prompt chaining

### Aplicaciones Especializadas

#### Prompts para Diferentes Dominios
- **Archivo**: `5-domain-specific-prompts.ipynb`
- Prompts técnicos (código, matemáticas)
- Prompts creativos (escritura, arte)
- Prompts analíticos (datos, investigación)
- Prompts de negocio (marketing, ventas)

#### Optimización y Evaluación
- **Archivo**: `6-prompt-optimization.ipynb`
- Métricas de evaluación
- A/B testing de prompts
- Iteración sistemática
- Herramientas de evaluación

### Mejores Prácticas

**Diseño de Prompts:**
1. **Claridad**: Instrucciones inequívocas
2. **Especificidad**: Detalles relevantes del contexto
3. **Estructura**: Formato consistente y lógico
4. **Ejemplos**: Representativos y diversos
5. **Limitaciones**: Restricciones claras cuando sea necesario

**Optimización:**
1. Iteración sistemática con cambios controlados
2. Métricas objetivas y medición cuantitativa
3. Set de casos de prueba diverso y representativo
4. Registro de experimentos
5. Validación cruzada con diferentes modelos

**Consideraciones Éticas:**
1. Identificar y mitigar sesgos en prompts
2. Explicar comportamiento del sistema
3. Proteger información sensible
4. Clarificar limitaciones del modelo

### Casos de Uso Empresariales

**Marketing y Ventas:**
- Generación de copy publicitario
- Análisis de sentimientos de clientes
- Personalización de comunicaciones
- Investigación de mercado automatizada

**Atención al Cliente:**
- Clasificación automática de tickets
- Generación de respuestas FAQ
- Escalamiento inteligente
- Análisis de satisfacción

**Recursos Humanos:**
- Screening inicial de CVs
- Generación de job descriptions
- Análisis de feedback de empleados
- Chatbots de políticas internas

**Investigación y Desarrollo:**
- Revisión de literatura científica
- Generación de hipótesis
- Análisis de patentes
- Documentación técnica

---

## 🔍 IL1.3: Infraestructura RAG (Retrieval-Augmented Generation)

### Descripción
Exploración de la arquitectura de Recuperación Aumentada por Generación (RAG), una técnica poderosa para conectar LLMs con fuentes de conocimiento externas y actualizadas.

### ¿Qué es RAG?
RAG es un enfoque que mejora las respuestas de los LLMs al permitirles consultar una base de conocimiento externa antes de generar una respuesta. Esto reduce las "alucinaciones" y asegura que la información proporcionada sea relevante y precisa.

### Contenido del Módulo

#### 1. Basic RAG
- **Archivo**: `1-basic-rag.ipynb`
- Conceptos fundamentales de RAG
- Ejemplo simple y práctico

#### 2. Text Chunking
- **Archivo**: `2-text-chunking.py`
- Diferentes estrategias para dividir texto en fragmentos
- Paso crucial para la eficiencia del recuperador

#### 3. Embeddings Simple RAG
- **Archivo**: `3-embeddings-simple-rag.ipynb`
- Generar embeddings a partir de fragmentos de texto
- Construcción de un sistema RAG básico

#### 4. Vector RAG
- **Archivo**: `4-vector-rag.ipynb`
- Implementación robusta con base de datos vectorial
- Almacenar y consultar eficientemente los embeddings

### Objetivos de Aprendizaje
- Comprender la arquitectura y componentes de un sistema RAG
- Implementar un flujo RAG básico para responder preguntas
- Aplicar técnicas de text chunking para procesar documentos
- Utilizar modelos de embeddings para convertir texto en vectores
- Integrar una base de datos vectorial para sistema RAG escalable

---

## 📊 IL1.4: Evaluación y Optimización de LLMs y RAG

### Descripción
Módulo centrado en la evaluación y optimización sistemática de sistemas de IA, con énfasis en sistemas RAG.

### Objetivos de Aprendizaje
- **Comprender la importancia** de la evaluación sistemática en sistemas RAG
- **Identificar y aplicar métricas clave**: Precisión del Contexto, Fidelidad de la Respuesta, Relevancia
- **Utilizar LangSmith** para trazabilidad, monitoreo y evaluación automatizada
- **Implementar ciclo de mejora continua**: evaluar, analizar y optimizar

### Métricas Clave

**Recuperación (Retrieval):**
- `Context Precision`: Precisión del contexto recuperado
- `Context Recall`: Cobertura del contexto relevante

**Generación (Generation):**
- `Faithfulness` (Fidelidad): La respuesta es fiel a la información recuperada
- `Answer Relevancy`: La respuesta es relevante a la pregunta

### Archivos y Actividades Prácticas

#### 1. Aplicación Interactiva con Streamlit
- **Archivo**: `1-evaluation-rag.py`
- Aplicación interactiva para visualizar sistema RAG en acción
- Modificar documentos, realizar consultas
- Ver métricas de rendimiento y calidad en tiempo real

#### 2. Evaluación con LangSmith
- **Archivo**: `2-langsmith-evaluation.ipynb`
- Configurar trazabilidad con LangSmith
- Crear dataset de evaluación con ground truth
- Ejecutar evaluadores automáticos
- Analizar resultados para identificar puntos débiles

### Cómo Empezar

1. **Configurar entorno**: Variables de API necesarias en archivo `.env`
2. **Explorar aplicación interactiva**:
   ```bash
   streamlit run RA1/IL1.4/1-evaluation-rag.py
   ```
3. **Realizar evaluación sistemática**: Ejecutar notebook de LangSmith
4. **Iterar y mejorar**: Modificar sistema y re-evaluar

---

## 🤖 RA2: Desarrollo de Agentes Inteligentes con LLM

### Descripción General
En la segunda experiencia de aprendizaje, los estudiantes desarrollan competencias avanzadas en la construcción de agentes inteligentes basados en LLM. Se enfatiza la comprensión del paradigma de agentes autónomos, la integración de herramientas externas, el manejo de memoria y las estrategias de planificación.

### Objetivos Principales
- Comprender arquitecturas de agentes LLM
- Diferenciar componentes: herramientas, memoria, planificación y ejecución
- Trabajar con frameworks especializados (LangChain, CrewAI)
- Explorar function calling e integración con APIs y bases de datos
- Implementar protocolos como MCP (Model Context Protocol)

### Evaluaciones RA2
- **Ev For 2**: Quiz Agentes de IA (8 preguntas)
- **Ev For 2**: Construcción de Agente Básico

---

## 🏗️ IL2.1: Arquitectura y Frameworks de Agentes

### Descripción
Exploración de los fundamentos de la arquitectura de agentes inteligentes basados en LLM, progresando desde implementaciones básicas hasta frameworks avanzados.

### Objetivos de Aprendizaje
- Comprender qué es un agente inteligente y sus componentes (cerebro, memoria, herramientas, planificación)
- Dominar el ciclo de razonamiento ReAct (Reason + Act)
- Implementar agentes desde cero y usando frameworks
- Configurar correctamente frameworks con GitHub Models API
- Diseñar equipos de agentes colaborativos
- Entender criterios de selección entre frameworks

### Contenido del Módulo

#### 1. Fundamentos de Agentes Inteligentes
- **Archivo**: `1-agent-fundamentals.ipynb`
- Conceptos fundamentales: cerebro, memoria, herramientas
- Ciclo ReAct (Reason + Act) manual
- Parsing de texto y gestión de estado
- Limitaciones y motivación para frameworks

#### 2. Function Calling Nativo
- **Archivo**: `2-agent-function-calling.ipynb`
- Mecanismo estructurado de OpenAI
- Definición de herramientas con JSON Schema
- Ventajas: confiabilidad, seguridad
- Flujo de llamadas estructuradas
- Integración con Wikipedia API

#### 3. Framework LangChain
- **Archivo**: `3-langchain-agent.ipynb`
- Abstracciones de alto nivel: `AgentExecutor`, `Tool`
- Configuración simplificada con decoradores
- Gestión automática de historial y errores
- Tipos de agentes: Zero-shot, Conversational, Structured

#### 4. Framework CrewAI
- **Archivo**: `4-crewai-agent.ipynb`
- Conceptos: Agent, Task, Crew, Process
- Especialización por roles: Investigador, Escritor
- Coordinación secuencial con dependencias
- **🔧 CONFIGURACIÓN CRÍTICA**: Mapeo de variables para GitHub Models API

### Configuraciones Técnicas Importantes

**Variables de Entorno Requeridas:**
```bash
export OPENAI_BASE_URL="https://models.inference.ai.azure.com"
export GITHUB_TOKEN="tu_token_de_github"
```

**Configuración para LangChain:**
```python
# LangChain funciona directamente con las variables estándar
llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

**Configuración para CrewAI (CRÍTICA):**
```python
# CrewAI requiere mapeo específico de variables
import os
os.environ["OPENAI_API_BASE"] = os.environ.get("OPENAI_BASE_URL", "")
os.environ["OPENAI_API_KEY"] = os.environ.get("GITHUB_TOKEN", "")
```

### Problemas Comunes y Soluciones

**1. Error de Autenticación en CrewAI**
- **Síntoma**: `AuthenticationError: Incorrect API key provided`
- **Causa**: CrewAI espera variables específicas
- **Solución**: Mapear `GITHUB_TOKEN` → `OPENAI_API_KEY`

**2. Error de Herramientas en CrewAI**
- **Síntoma**: `'Tool' object is not callable`
- **Causa**: Mezclar decorador `@tool` de LangChain con CrewAI
- **Solución**: Usar `BaseTool` de `crewai_tools`

**3. Error de Parámetro Verbose**
- **Síntoma**: `ValidationError: Input should be a valid boolean`
- **Causa**: Usar `verbose=2` en lugar de boolean
- **Solución**: Usar `verbose=True` en Crew

### Patrones Arquitectónicos

| **Patrón** | **Notebook** | **Características** |
|------------|--------------|-------------------|
| **Monolítico** | 1-agent-fundamentals | Toda la lógica en una función, parsing manual |
| **Estructurado** | 2-agent-function-calling | JSON Schema, llamadas nativas |
| **Modular** | 3-langchain-agent | Separación de componentes, abstracciones |
| **Colaborativo** | 4-crewai-agent | Múltiples agentes especializados |

### Comparación de Frameworks

| **Criterio** | **LangChain** | **CrewAI** |
|-------------|--------------|------------|
| **Especialización** | Agentes individuales complejos | Equipos colaborativos |
| **Complejidad** | Simple a moderada | Compleja, multi-paso |
| **Flexibilidad** | Muy alta, experimental | Estructurada, workflow-oriented |
| **Configuración** | Directa con variables estándar | Requiere mapeo específico |
| **Curva de aprendizaje** | Moderada | Baja para equipos |
| **Casos de uso** | Experimentación, prototipado | Workflows de producción |

---

## 💾 IL2.2: Sistemas de Memoria e Integración de Herramientas

### Descripción
Módulo centrado en dotar a los agentes de IA de **memoria**, capacidad crucial para pasar de interacciones simples a conversaciones coherentes y contextuales.

### Objetivos de Aprendizaje
- Comprender la importancia de la memoria conversacional
- Implementar diferentes estrategias de memoria
- Gestión de estado (Stateful vs. Stateless)
- Integración de herramientas externas (APIs, bases de datos)

### Contenido del Módulo

#### 1. Agentes con Memoria Conversacional
- **Archivo**: `1-memory-agent.ipynb`
- Concepto de memoria en agentes LangChain
- Historial de chat gestionado manualmente
- Responder preguntas de seguimiento
- Importancia del contexto en conversaciones

#### 2. Sistemas de Memoria Avanzados
- **Archivo**: `2-memory-agent-advanced.ipynb`
- Soluciones de memoria automatizadas de LangChain
- Tres estrategias clave:
  - **`ConversationBufferMemory`**: Historial completo
  - **`ConversationBufferWindowMemory`**: Últimas k interacciones
  - **`ConversationSummaryMemory`**: Resume el historial, ahorra tokens

### Conceptos Clave

**Memoria Conversacional:**
- Capacidad de retener y utilizar información de interacciones pasadas

**Gestión de Estado:**
- **Stateful**: El agente recuerda el contexto
- **Stateless**: El agente no mantiene contexto entre interacciones

**Estrategias de Memoria:**
- Diferentes enfoques para gestionar historial
- Ventajas y casos de uso específicos (Buffer, Window, Summary)

**Integración de Herramientas:**
- Capacidad de usar herramientas externas
- APIs, bases de datos, servicios web
- Obtener información del mundo real

---

## 🎯 IL2.3: Planificación y Orquestación

### Descripción
Exploración de estrategias avanzadas de planificación y orquestación para agentes LLM, incluyendo planificación jerárquica, coordinación multi-agente y gestión de flujos de trabajo complejos.

### Objetivos de Aprendizaje
- Comprender diferentes estrategias de planificación para agentes
- Implementar planificación jerárquica y reactiva
- Diseñar sistemas de orquestación multi-agente
- Gestionar flujos de trabajo complejos y dependencias
- Optimizar la coordinación entre agentes especializados

### Contenido del Módulo

#### 1. Estrategias de Planificación
- `1-planning-strategies.py` - Tipos de planificación y algoritmos
- `2-hierarchical-planning.py` - Planificación jerárquica
- `3-reactive-planning.py` - Planificación reactiva
- `4-goal-oriented-planning.py` - Planificación orientada a objetivos

#### 2. Orquestación de Agentes
- `5-agent-orchestration.py` - Coordinación de agentes
- `6-workflow-management.py` - Gestión de flujos de trabajo
- `7-task-decomposition.py` - Descomposición de tareas
- `8-resource-allocation.py` - Asignación de recursos

#### 3. Coordinación Avanzada
- `9-multi-agent-coordination.py` - Coordinación multi-agente
- `10-conflict-resolution.py` - Resolución de conflictos
- `11-negotiation-strategies.py` - Estrategias de negociación
- `12-emergence-behaviors.py` - Comportamientos emergentes

---

## 📝 IL2.4: Documentación Técnica y Diseño de Arquitectura

### Descripción
Mejores prácticas para documentar sistemas de agentes LLM y diseñar arquitecturas escalables, incluyendo patrones de diseño, documentación técnica y estrategias de implementación.

### Objetivos de Aprendizaje
- Comprender patrones de arquitectura para sistemas de agentes
- Crear documentación técnica efectiva
- Diseñar arquitecturas escalables y mantenibles
- Implementar patrones de diseño para agentes
- Gestionar la evolución y mantenimiento de sistemas

### Contenido del Módulo

#### 1. Patrones de Arquitectura
- `1-architecture-patterns.py` - Patrones de diseño para agentes
- `2-scalable-architectures.py` - Arquitecturas escalables
- `3-microservices-agents.py` - Agentes en microservicios
- `4-event-driven-agents.py` - Agentes basados en eventos

#### 2. Documentación Técnica
- `5-technical-documentation.py` - Generación de documentación
- `6-api-documentation.py` - Documentación de APIs
- `7-architecture-diagrams.py` - Diagramas de arquitectura
- `8-code-documentation.py` - Documentación de código

#### 3. Gestión y Mantenimiento
- `9-version-control.py` - Control de versiones para agentes
- `10-testing-strategies.py` - Estrategias de testing
- `11-deployment-patterns.py` - Patrones de despliegue
- `12-monitoring-observability.py` - Monitoreo y observabilidad

### Mejores Prácticas

**Arquitectura:**
- Usar nombres claros para clases y funciones
- Documentar cada función con docstrings
- Separar la lógica del agente y las herramientas
- Usar control de versiones (Git)
- Escribir ejemplos de uso en el archivo principal

**Patrones de Diseño:**
- Clean Architecture
- Microservices Patterns
- Event-Driven Architecture

---

## 🔒 RA3: Observabilidad, Seguridad y Ética en Agentes de IA

### Descripción General
En la tercera experiencia de aprendizaje, los estudiantes desarrollan competencias críticas en observabilidad, seguridad y consideraciones éticas para agentes de IA. Se enfatiza la implementación de herramientas de monitoreo, análisis de trazabilidad y aplicación de buenas prácticas éticas.

### Objetivos Principales
- Implementar herramientas de monitoreo para agentes
- Analizar métricas de desempeño y trazabilidad
- Aplicar protocolos de seguridad
- Trabajar con herramientas especializadas de observabilidad
- Explorar análisis de logs y detección de anomalías
- Optimización basada en datos observados
- Garantizar escalabilidad, seguridad y sostenibilidad en producción

### Evaluaciones RA3
- **Ev For 3**: Quiz Observabilidad y Trazabilidad (8 preguntas)
- **Ev For 3**: Implementación de Observabilidad

---

## 📊 IL3.1: Herramientas de Observabilidad y Métricas

### Descripción
Módulo para aprender a agregar logs y métricas básicas a los agentes de IA para monitorear su funcionamiento y desempeño.

### Contenido Principal
- **Archivo**: `1-observability_tools.py`
- Ejemplo de logging
- Medición de tiempo de respuesta
- Importancia de registrar eventos clave
- Detección de problemas en tiempo real

### Conceptos Clave
- **Logging**: Registro de eventos y acciones del agente
- **Métricas**: Mediciones cuantitativas de desempeño
- **Tiempo de Respuesta**: Latencia y performance
- **Eventos Clave**: Identificación de puntos críticos para monitoreo

---

## 🔍 IL3.2: Análisis de Trazabilidad y Logs

### Descripción
Módulo que muestra cómo registrar y analizar logs para entender el comportamiento de los agentes.

### Contenido Principal
- **Archivo**: `1-traceability_analysis.py`
- Ejemplo de guardado y lectura de logs
- Análisis de patrones en logs
- Utilidad de la trazabilidad para depuración
- Auditoría de sistemas de agentes

### Conceptos Clave
- **Trazabilidad**: Capacidad de seguir el flujo de ejecución
- **Análisis de Logs**: Interpretación de registros históricos
- **Depuración**: Uso de logs para identificar y resolver problemas
- **Auditoría**: Registro para cumplimiento y revisión

---

## 🛡️ IL3.3: Seguridad y Ética en Agentes de IA

### Descripción
Aprendizaje de buenas prácticas básicas para proteger agentes y actuar de forma ética.

### Contenido Principal
- **Archivo**: `1-security_ethics.py`
- Validación de entradas
- Respuestas responsables
- Importancia de evitar acciones peligrosas
- Consideraciones éticas en agentes autónomos

### Conceptos Clave
- **Validación de Entradas**: Prevención de inyecciones maliciosas
- **Respuestas Responsables**: Evitar contenido dañino o sesgado
- **Ética en IA**: Principios de uso responsable
- **Seguridad**: Protección contra vulnerabilidades

### Consideraciones Éticas
1. **Transparencia**: Claridad sobre capacidades y limitaciones
2. **Privacy**: Protección de datos sensibles
3. **Fairness**: Evitar sesgos y discriminación
4. **Accountability**: Responsabilidad en las acciones del agente
5. **Safety**: Prevención de daños

---

## ⚙️ IL3.4: Escalabilidad y Sostenibilidad

### Descripción
Recomendaciones para que los agentes sean escalables y sostenibles en producción.

### Contenido Principal
- **Archivo**: `1-scalability_sustainability.py`
- Consejos para dividir el sistema
- Monitorear recursos
- Automatizar despliegues
- Importancia de la eficiencia
- Mantenimiento a largo plazo

### Conceptos Clave

**Escalabilidad:**
- **Horizontal Scaling**: Agregar más instancias
- **Vertical Scaling**: Aumentar recursos de instancia existente
- **Load Balancing**: Distribución de carga
- **Caching**: Optimización de respuestas frecuentes

**Sostenibilidad:**
- **Eficiencia de Recursos**: Uso optimizado de CPU/memoria
- **Mantenibilidad**: Código limpio y documentado
- **Automatización**: CI/CD para despliegues
- **Monitoreo Continuo**: Alertas y observabilidad

---

## 🎓 Evaluación Transversal

### Proyecto Final (40% de la nota)
- **Alcance**: Cubre todos los resultados de aprendizaje (RA1, RA2, RA3)
- **Formato**: Proyecto práctico + presentación
- **Requisitos**:
  - Implementación de un agente inteligente completo
  - Documentación técnica y arquitectura
  - Sistema de observabilidad implementado
  - Consideraciones de seguridad y ética
  - Evaluación de desempeño con métricas

### Evaluaciones Formativas
- **Quizzes**: 8 preguntas por cada RA (conceptos teóricos)
- **Proyectos Prácticos**: Implementaciones y presentaciones
- **Trabajo en Parejas**: Desarrollo colaborativo con presentaciones individuales

---

## 🛠️ Stack Tecnológico del Curso

### Lenguajes y Entornos
- **Python 3.8+**: Lenguaje principal
- **Jupyter Notebook**: Notebooks interactivos (.ipynb)
- **Streamlit**: Aplicaciones de demostración

### Frameworks y Librerías

**LLM y Agentes:**
- `openai`: Cliente para API de OpenAI
- `langchain` y `langchain-openai`: Framework para agentes LLM
- `crewai`: Framework para equipos de agentes

**Observabilidad:**
- `langsmith`: Trazabilidad y evaluación
- `langfuse`: Observabilidad de agentes
- `arize`: Monitoring de modelos de IA

**Utilidades:**
- `pandas`: Manipulación de datos
- `requests`: Llamadas HTTP
- Bibliotecas estándar de Python

### APIs y Servicios
- **GitHub Models API**: Acceso a modelos LLM
- **OpenAI-compatible APIs**: Integración unificada
- **LangSmith**: Plataforma de evaluación y monitoreo

---

## 📋 Variables de Entorno Necesarias

```bash
# Configuración de APIs
export GITHUB_BASE_URL="https://models.inference.ai.azure.com"
export GITHUB_TOKEN="tu_token_de_github"
export OPENAI_BASE_URL="https://models.inference.ai.azure.com"
export OPENAI_API_KEY="tu_api_key"

# Para CrewAI (mapeo específico)
export OPENAI_API_BASE="https://models.inference.ai.azure.com"

# Para LangSmith (opcional)
export LANGSMITH_API_KEY="tu_langsmith_api_key"
```

---

## 🎯 Flujo de Aprendizaje Recomendado

### 1. Fundamentos (RA1)
1. **IL1.1**: Conexión a APIs y conceptos básicos de LLMs
2. **IL1.2**: Técnicas de prompting efectivo
3. **IL1.3**: Infraestructura RAG para conocimiento externo
4. **IL1.4**: Evaluación y optimización de sistemas

### 2. Agentes Inteligentes (RA2)
1. **IL2.1**: Arquitectura y frameworks de agentes
2. **IL2.2**: Sistemas de memoria e integración de herramientas
3. **IL2.3**: Planificación y orquestación
4. **IL2.4**: Documentación técnica y diseño de arquitectura

### 3. Producción (RA3)
1. **IL3.1**: Herramientas de observabilidad y métricas
2. **IL3.2**: Análisis de trazabilidad y logs
3. **IL3.3**: Seguridad y ética en agentes de IA
4. **IL3.4**: Escalabilidad y sostenibilidad

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [LangChain Docs](https://python.langchain.com/)
- [CrewAI Docs](https://docs.crewai.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [GitHub Models](https://github.com/marketplace/models)

### Guías y Tutoriales
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
- [LangChain Prompt Hub](https://smith.langchain.com/hub)
- [OpenAI Cookbook](https://cookbook.openai.com/)

### Comunidades
- r/PromptEngineering (Reddit)
- Prompt Engineering Discord
- AI Alignment Forum
- Hugging Face Community
- LangChain Community (GitHub Discussions)

### Arquitectura y Patrones
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Microservices Patterns](https://microservices.io/patterns/)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)

### Investigación Académica
- [Chain-of-Thought Prompting Paper](https://arxiv.org/abs/2201.11903)
- [Few-Shot Learning Research](https://arxiv.org/abs/2005.14165)
- [Transformer Architecture Paper](https://arxiv.org/abs/1706.03762)

---

## 💡 Conclusión

Este curso proporciona una formación completa en el desarrollo de soluciones de IA basadas en LLMs, desde los fundamentos hasta la producción:

### Habilidades Adquiridas

**Fundamentos (RA1):**
- ✅ Conexión y uso de APIs de LLMs
- ✅ Técnicas avanzadas de prompt engineering
- ✅ Implementación de sistemas RAG
- ✅ Evaluación y optimización de sistemas LLM

**Agentes Inteligentes (RA2):**
- ✅ Construcción de agentes desde cero
- ✅ Uso de frameworks (LangChain, CrewAI)
- ✅ Sistemas de memoria conversacional
- ✅ Planificación y orquestación multi-agente
- ✅ Documentación técnica y arquitectura

**Producción (RA3):**
- ✅ Implementación de observabilidad
- ✅ Análisis de trazabilidad y logs
- ✅ Aplicación de principios de seguridad y ética
- ✅ Escalabilidad y sostenibilidad

### Perfil del Egresado

Al completar este curso, los estudiantes estarán capacitados para:

1. **Diseñar e implementar** soluciones de IA generativa en contextos organizacionales
2. **Desarrollar agentes inteligentes** complejos y equipos multi-agente
3. **Aplicar mejores prácticas** de ingeniería de software a sistemas de IA
4. **Evaluar y optimizar** sistemas LLM con métricas objetivas
5. **Llevar soluciones a producción** con observabilidad, seguridad y escalabilidad

---

**Estructura del Repositorio:**
```
RA1/  # Fundamentos de IA Generativa y Prompt Engineering
  IL1.1/  # Introducción a LLMs y APIs
  IL1.2/  # Técnicas de prompting
  IL1.3/  # Infraestructura RAG
  IL1.4/  # Evaluación y optimización

RA2/  # Desarrollo de Agentes Inteligentes
  IL2.1/  # Arquitectura y frameworks (LangChain, CrewAI)
  IL2.2/  # Memoria y herramientas externas
  IL2.3/  # Planificación y orquestación
  IL2.4/  # Documentación técnica y arquitectura

RA3/  # Observabilidad, Seguridad y Ética
  IL3.1/  # Observabilidad y métricas
  IL3.2/  # Trazabilidad y logs
  IL3.3/  # Seguridad y ética
  IL3.4/  # Escalabilidad y sostenibilidad
```

---

*Este documento proporciona un resumen completo de todos los módulos del curso para facilitar la contextualización de sistemas de IA sobre el contenido completo del programa educativo.*
