import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# 1. Загружаем ключи
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY", "")

print("🔍 Подключаемся к базе Qdrant...")

# 2. Инициализируем ту же модель эмбеддингов
embeddings = OpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    model="baai/bge-m3"
)

# 3. Подключаемся к коллекции
qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="mobilesmarts_knowledge",
    url="http://localhost:6333",
    prefer_grpc=False
)

# 4. ДЕЛАЕМ ПРЯМОЙ ПОИСК (Как обычный SELECT в SQL)
query = "Код и логика операции ОснПроцесс"
print(f"\nИщем строку: '{query}'\n")

# Просим базу выдать 5 самых близких результатов без всякой фильтрации
results = qdrant.similarity_search(query, k=5)

if not results:
    print("❌ База пуста или ничего не найдено!")
else:
    for i, doc in enumerate(results):
        file_name = doc.metadata.get('source', 'Unknown').split('\\')[-1].split('/')[-1]
        print(f"--- Результат {i+1} (из {file_name}) ---")
        # Печатаем первые 300 символов, чтобы не засорять экран
        print(doc.page_content[:300] + "...\n")