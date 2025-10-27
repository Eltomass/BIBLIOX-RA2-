# LibreriaX - Sistema de Gestión de Biblioteca con IA

Este proyecto implementa un sistema completo de gestión de biblioteca con inteligencia artificial, incluyendo un frontend en React y un backend en Python.

## Características Principales

- **Frontend React**: Interfaz moderna y responsive para la gestión de libros, préstamos y usuarios
- **Backend Python**: API REST con capacidades de IA para consultas inteligentes
- **Sistema RAG**: Recuperación y generación aumentada para respuestas contextuales
- **Gestión de Transacciones**: Sistema completo de préstamos, multas y pagos

## Estructura del Proyecto

```
libreriax/
├── src/                    # Frontend React
│   ├── components/         # Componentes reutilizables
│   ├── pages/             # Páginas principales
│   ├── hooks/             # Custom hooks
│   └── services/          # Servicios de API
├── backend/               # Backend Python
│   ├── src/
│   │   ├── api.py         # API principal
│   │   ├── models/        # Modelos de IA
│   │   ├── rag/           # Sistema RAG
│   │   └── data/          # Datos de la biblioteca
│   └── streamlit_app.py   # Interfaz Streamlit
└── public/                # Archivos estáticos
```

## Tecnologías Utilizadas

- **Frontend**: React, Tailwind CSS, JavaScript
- **Backend**: Python, FastAPI, Streamlit
- **IA**: LLM, RAG (Retrieval-Augmented Generation)
- **Base de Datos**: Archivos de texto estructurados

## Instalación y Configuración

### Frontend (React)

```bash
npm install
npm start
```

El frontend estará disponible en [http://localhost:3000](http://localhost:3000)

### Backend (Python)

```bash
cd backend
pip install -r requirements.txt
python src/api.py
```

### Interfaz Streamlit

```bash
cd backend
streamlit run streamlit_app.py
```

## Scripts Disponibles

### Frontend
- `npm start`: Ejecuta la aplicación en modo desarrollo
- `npm test`: Ejecuta las pruebas
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