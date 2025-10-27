import streamlit as st
from src.rag.indexing.indexer import build_or_load_vectorstore
from src.rag.retrieval.retriever import retrieve_relevant
from src.utils.formatting import format_context
from src.rag.generation.generator import generate_answer
from src.agents.router import detect_domain

st.set_page_config(page_title="Sistema RAG Librería", page_icon="📚", layout="wide")
st.title("🤖 Asistente Virtual de Librería")

@st.cache_resource(show_spinner=False)
def get_vectorstore():
	return build_or_load_vectorstore()

vs = get_vectorstore()

with st.sidebar:
	st.header("⚙️ Configuración RAG")
	k = st.slider("Documentos a recuperar (k)", 1, 8, 4)
	st.caption("Modelo: llama3.1:8b en Ollama")
	st.divider()
	upload = st.file_uploader("Cargar documentos internos (.txt)", type=["txt"], accept_multiple_files=True)
	if upload:
		# ingestión rápida (no persistente en demo)
		texts = [f.read().decode('utf-8') for f in upload]
		from langchain_community.vectorstores import Chroma
		from src.models.llm import get_embeddings
		emb = get_embeddings()
		for t in texts:
			vs.add_texts([t], embedding=emb)
		st.success(f"Ingeridos {len(texts)} documentos.")

col_chat, col_sources = st.columns([2, 1])

with col_chat:
	st.subheader("Chat")
	if "messages" not in st.session_state:
		st.session_state.messages = []
	for m in st.session_state.messages:
		st.chat_message(m["role"]).markdown(m["content"]) 

	q = st.chat_input("Escribe tu consulta…")
	if q:
		st.session_state.messages.append({"role": "user", "content": q})
		domain = detect_domain(q)
		retrieved = retrieve_relevant(vs, q, k=k)
		ctx = format_context(retrieved)
		answer = generate_answer(q, ctx, domain=domain)
		st.session_state.messages.append({"role": "assistant", "content": answer})
		st.experimental_rerun()

with col_sources:
	st.subheader("Fuentes y Métricas")
	if 'last_retrieved' not in st.session_state:
		st.session_state.last_retrieved = []
	# Mostrar últimas fuentes usadas
	if st.session_state.messages:
		# Re-ejecutar recuperación para mostrar contexto del último user
		last_user = next((m for m in reversed(st.session_state.messages) if m['role']=='user'), None)
		if last_user:
			retrieved = retrieve_relevant(vs, last_user['content'], k=k)
			st.session_state.last_retrieved = retrieved
	for text, score in st.session_state.last_retrieved:
		with st.expander(f"score={score:.3f}"):
			st.write(text)

st.caption("Demo académica - LibreriaX RAG + LLM (Ollama)")
