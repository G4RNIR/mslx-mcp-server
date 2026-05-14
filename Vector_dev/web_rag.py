import os
import requests
import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --- Функция автоопределения моделей из Ollama ---
def get_active_models(base_url: str):
    """Опрашивает сервер Ollama по стандарту OpenAI API"""
    try:
        response = requests.get(f"{base_url}/models", timeout=2)
        if response.status_code == 200:
            models_data = response.json().get("data", [])
            return [model["id"] for model in models_data]
    except requests.exceptions.RequestException:
        pass
    return []

st.set_page_config(page_title="MobileSmarts RAG", page_icon="🧠", layout="wide")
st.title("🧠 База знаний MobileSmarts (Ollama Edition)")

# --- Боковая панель ---
with st.sidebar:
    st.header("⚙️ Настройки")
    
    st.subheader("1. LLM Сервер (Ollama)")
    # Стандартный порт Ollama - 11434
    lm_url = st.text_input("URL сервера", value="http://localhost:11434/v1")
    
    available_models = get_active_models(lm_url)
    if available_models:
        st.success("Ollama работает!")
        lm_name = st.selectbox("Загруженная модель", available_models)
    else:
        st.error("Ollama не отвечает. Убедитесь, что программа запущена.")
        lm_name = st.text_input("Имя модели (fallback)", value="qwen2.5:latest")
    
    st.subheader("2. Векторизация (Embeddings)")
    embed_model_name = st.selectbox(
        "Модель (скачается автоматически через Python)",
        ["intfloat/multilingual-e5-large", "BAAI/bge-m3"]
    )
    
    st.subheader("3. База данных")
    data_dir_input = st.text_input("Путь к документам (.md)", value=str(Path.cwd() / "docs"))
    index_button = st.button("🔄 Индексировать базу", use_container_width=True)

# --- Инициализация RAG ---
@st.cache_resource(show_spinner=False)
def load_rag_chain(lm_url, lm_name, embed_model_name):
    try:
        # Подключаемся к Ollama как к OpenAI
        llm = ChatOpenAI(
            base_url=lm_url,
            api_key="ollama", # ключ не важен
            model=lm_name,
            temperature=0.1,
            streaming=True
        )
        
        embeddings = HuggingFaceEmbeddings(model_name=embed_model_name)
        
        qdrant = Qdrant.from_existing_collection(
            embedding=embeddings,
            collection_name="mobilesmarts_knowledge",
            url="http://localhost:6333",
            prefer_grpc=False
        )
        
        base_retriever = qdrant.as_retriever(search_kwargs={"k": 20})
        compressor = FlashrankRerank(top_n=5)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, 
            base_retriever=base_retriever
        )
        
        system_prompt = (
            "Ты — технический эксперт по платформе MobileSmarts. "
            "Отвечай на вопросы только на основе контекста ниже. "
            "Если информации нет — скажи об этом прямо.\n\n"
            "Контекст:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        return create_retrieval_chain(compression_retriever, question_answer_chain)
    except Exception as e:
        return None

# --- Логика индексации ---
if index_button:
    with st.spinner("Векторизация данных... Это может занять пару минут."):
        target_dir = Path(data_dir_input)
        if not target_dir.exists():
            st.error(f"Папка {target_dir} не найдена!")
        else:
            loader = DirectoryLoader(str(target_dir), glob="**/*.md", loader_cls=TextLoader)
            documents = loader.load()
            
            if documents:
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n## Блок:", "\n\n", "\n", " "])
                chunks = text_splitter.split_documents(documents)
                
                embeddings_init = HuggingFaceEmbeddings(model_name=embed_model_name)
                Qdrant.from_documents(
                    documents=chunks,
                    embedding=embeddings_init,
                    url="http://localhost:6333",
                    collection_name="mobilesmarts_knowledge",
                    force_recreate=True,
                    prefer_grpc=False
                )
                st.success(f"База обновлена! Загружено {len(chunks)} блоков.")
                st.cache_resource.clear()
            else:
                st.warning("В папке нет .md файлов.")

# --- Чат ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

rag_chain = load_rag_chain(lm_url, lm_name, embed_model_name)

if prompt := st.chat_input("Ваш вопрос по базе MobileSmarts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not rag_chain:
            st.error("Система не готова. Проверьте запуск Ollama и Qdrant (Docker).")
        else:
            with st.spinner("Поиск в базе и генерация ответа..."):
                response = rag_chain.invoke({"input": prompt})
                answer = response['answer']
                st.markdown(answer)
                
                sources = set([Path(doc.metadata.get('source', 'Unknown')).name for doc in response["context"]])
                st.caption(f"Источники: {', '.join(sources)}")
                
                st.session_state.messages.append({"role": "assistant", "content": answer})