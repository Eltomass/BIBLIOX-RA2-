# Backend RAG - LibreriaX

Asistente RAG (LangChain + Chroma + Streamlit) y API FastAPI para integrar con el frontend.

## Prerrequisitos

- Windows 10/11 con PowerShell
- Python 3.12 (instalado con winget)
- Ollama funcionando en `http://localhost:11434` con modelo `llama3.1:8b`
- Microsoft C++ Build Tools (necesarios para compilar `chroma-hnswlib`)

### Instalar Python 3.12
```powershell
winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
```

### Configurar modelos de Ollama (opcional)
Por defecto, Ollama usa su carpeta estándar de modelos (en Windows: `%USERPROFILE%\.ollama\models`). NO es necesario cambiarla.

Si tienes los modelos en otra unidad o ruta, puedes sobrescribirla opcionalmente con la variable de entorno `OLLAMA_MODELS` y luego abrir una nueva ventana de PowerShell para que tome efecto:
```powershell
setx OLLAMA_MODELS "D:\ruta\a\mis\modelos"
# Abre una nueva PowerShell
ollama serve
ollama list
```

## Estructura
```
backend/
├── src/
│   ├── agents/              # router de dominio
│   ├── rag/
│   │   ├── indexing/        # indexación y persistencia en Chroma
│   │   ├── retrieval/       # búsqueda y ranking
│   │   └── generation/      # prompts y generación con LLM
│   ├── data/                # documentos internos mock
│   ├── models/              # configuración LLM/embeddings
│   └── utils/               # utilidades
├── streamlit_app.py         # app RAG
├── src/api.py               # API FastAPI mínima (chat via Ollama HTTP)
├── requirements.txt         # dependencias RAG (LangChain/Chroma/Streamlit)
└── README.md
```

## Ejecución Rápida (todo junto)

Desde la raíz del proyecto (donde está `package.json`):
```powershell
npm install
npm run dev
```
Esto lanza en paralelo:
- Frontend (CRA): `http://localhost:3000`
- Backend FastAPI (chat mínimo): `http://localhost:8000/docs`
- Streamlit (RAG): `http://localhost:8501`

Notas:
- Los scripts crean la venv (Python 3.12) y auto-instalan dependencias.
- Si la instalación de Streamlit/LangChain/Chroma falla por compilación, revisa "Solución de problemas".

## Ejecución Manual (solo backend)

Crear venv (Python 3.12), instalar dependencias y lanzar FastAPI mínimo:
```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python -m ensurepip --upgrade
.\.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python -m pip install fastapi uvicorn pydantic python-dotenv requests
.\.venv\Scripts\python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```
- Probar en `http://localhost:8000/docs` → POST `/api/chat`

Lanzar Streamlit (RAG completo, requiere Build Tools):
```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run streamlit_app.py
```
- Abrir `http://localhost:8501`

## Integración con Frontend

El frontend consume por defecto la API FastAPI mínima (`http://localhost:8000/api/chat`).
- Archivo: `src/services/chatAPI.js`
- Para apuntar a otra URL, crea `.env` en la raíz del proyecto:
```
REACT_APP_API_BASE=http://localhost:8000
```

Si deseas que el chat del frontend use el pipeline RAG (en vez del endpoint mínimo), añade un endpoint en FastAPI que orqueste la recuperación con LangChain/Chroma y la generación con LLM (ref. módulos en `src/rag/*`) y cambia `chatAPI.js` a ese endpoint.

## Datos internos mock
- `src/data/políticas_prestamos.txt`
- `src/data/reglamento_multas.txt`
- `src/data/catalogo_libros.txt`
- `src/data/procedimientos.txt`

## Modelo LLM y Embeddings
- LLM: `llama3.1:8b` (Ollama, `http://localhost:11434`)
- Embeddings: `OllamaEmbeddings` (o fallback `SentenceTransformer`)

## Solución de Problemas

- "No module named pip" en venv
  - Ejecuta: 
    ```powershell
    .\.venv\Scripts\python -m ensurepip --upgrade
    .\.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
    ```

- Compilación falla con `chroma-hnswlib`: "Microsoft Visual C++ 14.0 or greater is required"
  - Instala Microsoft C++ Build Tools (ver Prerrequisitos) y reintenta.

- Ollama no encuentra modelos o falta espacio en disco
  - Usa la ruta por defecto de Ollama o define `OLLAMA_MODELS` con tu ruta de modelos (ver arriba) y abre nueva PowerShell.
  - Libera espacio (8+ GB) si necesitas descargar modelos.

- Chat del frontend repite el texto / no responde
  - Verifica que `http://localhost:8000/docs` funcione y que `ollama serve` esté activo.
  - Revisa `.env` del frontend y que `REACT_APP_API_BASE` apunte a la URL correcta.

## Créditos

Hecho por: **Tomas Brogi** y **David Martinez**.
