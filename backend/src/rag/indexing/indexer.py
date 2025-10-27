import os
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from ..retrieval.schema import LIBRARY_METADATA
from ...models.llm import get_embeddings

CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.chroma'))
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

"""
IL1.2 - Pipeline RAG con Fuentes Internas
- Carga de documentos de políticas/procedimientos/catálogos y chunking.
- Vectorización y persistencia en Chroma para recuperación semántica.

IL1.3 - Control de contexto
- Splitter con tamaño/overlap adecuados para mejorar recuperación y evitar desbordar contexto del LLM.
"""

def load_internal_docs() -> List[str]:
	paths = [
		os.path.join(DATA_DIR, 'políticas_prestamos.txt'),
		os.path.join(DATA_DIR, 'reglamento_multas.txt'),
		os.path.join(DATA_DIR, 'catalogo_libros.txt'),
		os.path.join(DATA_DIR, 'procedimientos.txt'),
	]
	docs = []
	for p in paths:
		if os.path.exists(p):
			with open(p, 'r', encoding='utf-8') as f:
				docs.append(f.read())
	return docs


def chunk_texts(texts: List[str]):
	# Heurística de chunking: prioriza separadores de párrafo y líneas
	splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=180, separators=["\n\n", "\n", ". "])
	chunks = []
	for t in texts:
		chunks.extend(splitter.split_text(t))
	return chunks


def build_or_load_vectorstore():
	# Crea/carga el vector store persistente
	os.makedirs(CHROMA_DIR, exist_ok=True)
	emb = get_embeddings()
	texts = load_internal_docs()
	if not texts:
		return Chroma(collection_name="libreriax", embedding_function=emb, persist_directory=CHROMA_DIR)
	chunks = chunk_texts(texts)
	metadatas = [LIBRARY_METADATA for _ in chunks]
	vs = Chroma.from_texts(chunks, embedding=emb, collection_name="libreriax", metadatas=metadatas, persist_directory=CHROMA_DIR)
	vs.persist()
	return vs
