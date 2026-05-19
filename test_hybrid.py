import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

# === НАСТРОЙКИ ===
TARGET_DIR = r"E:\mcp-ms\Склад 15, Расширенный 19\Documents\Cleaned_Markdown"
QUERY = "ОснПроцесс"
# =================

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY", "")

print(f"📂 Загружаем файлы из: {TARGET_DIR}...")
loader = DirectoryLoader(TARGET_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
docs = loader.load()

print("✂️ Нарезаем текст и вшиваем имена файлов...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["## Блок:", "\n\n", "\n", " "])
chunks = text_splitter.split_documents(docs)

# Магия: привязываем имя файла к каждому куску текста
for chunk in chunks:
    file_name = Path(chunk.metadata.get('source', 'Unknown')).name
    chunk.page_content = f"Файл_источник: {file_name}\n" + chunk.page_content

print("⚙️ Настраиваем BM25 (Лексический поиск по буквам)...")
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

print("🧠 Подключаемся к Qdrant (Векторный поиск по смыслу)...")
embeddings = OpenAIEmbeddings(
    openai_api_key=api_key if api_key else "empty",
    openai_api_base="https://openrouter.ai/api/v1",
    model="baai/bge-m3"
)
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="mobilesmarts_knowledge",
    url="http://localhost:6333",
    prefer_grpc=False
)
qdrant_retriever = qdrant.as_retriever(search_kwargs={"k": 5})

print("🤝 Объединяем в ГИБРИДНЫЙ ПОИСК (70% точность, 30% смысл)...")
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, qdrant_retriever], 
    weights=[0.7, 0.3]
)

print(f"\n🔍 ИЩЕМ: '{QUERY}'\n")
results = hybrid_retriever.invoke(QUERY)

if not results:
    print("❌ Ничего не найдено!")
else:
    for i, doc in enumerate(results):
        file_name = Path(doc.metadata.get('source', 'Unknown')).name
        print(f"--- Место {i+1} (из файла {file_name}) ---")
        # Выводим первые 300 символов для компактности
        print(doc.page_content[:300] + "...\n")