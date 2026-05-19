import os
import sys
# --- ФОРСИРУЕМ UTF-8 ДЛЯ WINDOWS ---
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
# -----------------------------------

from dotenv import load_dotenv 
load_dotenv()                  
import requests
import streamlit as st
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
# Используем новую версию Qdrant, как обсуждали ранее
from langchain_qdrant import QdrantVectorStore as Qdrant 
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# --- Вспомогательные функции ---
def get_active_models(base_url: str):
    try:
        response = requests.get(f"{base_url}/models", timeout=2)
        if response.status_code == 200:
            return [model["id"] for model in response.json().get("data", [])]
    except requests.exceptions.RequestException:
        pass
    return []

def load_system_prompt():
    prompt_path = Path("RAG_System_prompt.md")
    if not prompt_path.exists():
        default_prompt = "Ты — технический эксперт по MobileSmarts.\nИспользуй только контекст.\n\n[Контекст]:\n{context}"
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(default_prompt)
        return default_prompt
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

# --- Интерфейс ---
st.set_page_config(page_title="MobileSmarts RAG", page_icon="🧠", layout="wide")
st.title("🧠 База знаний MobileSmarts")

with st.sidebar:
    st.header("⚙️ Настройки")
    
    st.subheader("1. LLM Генератор (Ответы)")
    llm_mode = st.radio("Режим работы модели:", ["Облако (API)", "Локально (Ollama)"])
    
    if llm_mode == "Локально (Ollama)":
        lm_url = st.text_input("URL сервера Ollama", value="http://localhost:11434/v1")
        api_key = "ollama_local" 
        
        available_models = get_active_models(lm_url)
        if available_models:
            st.success("✅ Ollama на связи!")
            lm_name = st.selectbox("Загруженная модель", available_models)
        else:
            st.error("❌ Ollama не отвечает.")
            lm_name = st.text_input("Имя модели (fallback)", value="qwen2.5:latest")
            
    else: 
        lm_url = st.text_input("URL API", value="https://openrouter.ai/api/v1")
        
        # Подхватываем тот же ключ, что используется для векторизации
        api_key = st.text_input(
            "API Ключ (OpenRouter)", 
            type="password", 
            value=os.getenv("OPENROUTER_API_KEY", "")
        )
        
        lm_name = st.text_input("Имя модели", value="google/gemini-2.5-flash")
        
    st.subheader("2. Векторизация (Облако OpenRouter)")
    # Мы убираем выбор локальных моделей и жестко фиксируем лучшую
    or_api_key = st.text_input("OpenRouter API Key (для векторов)", type="password", value=os.getenv("OPENROUTER_API_KEY", ""))
    embed_model_name = "baai/bge-m3"

    st.subheader("3. Индексация базы")
    data_dir_input = st.text_input("Путь к чистым .md файлам", value=str())
    
    # КНОПКА ИНИЦИАЛИЗАЦИИ
    st.markdown("---")
    if st.button("🚀 ПОДКЛЮЧИТЬ ИИ", type="primary", use_container_width=True):
        st.session_state['system_ready'] = False
        with st.spinner("Загрузка моделей в память..."):
            try:
                sys_prompt_text = load_system_prompt()
                
                llm = ChatOpenAI(
                    base_url=lm_url,
                    api_key=api_key if api_key else "empty", 
                    model=lm_name,
                    temperature=0.1,
                    streaming=True
                )
                
                embeddings = OpenAIEmbeddings(
                    openai_api_key=or_api_key if or_api_key else "empty",
                    openai_api_base="https://openrouter.ai/api/v1",
                    model=embed_model_name
                )
                
                qdrant = Qdrant.from_existing_collection(
                    embedding=embeddings,
                    collection_name="mobilesmarts_knowledge",
                    url="http://localhost:6333",
                    prefer_grpc=False
                )
                
                # 1. Векторный поиск Qdrant (Поиск по смыслу)
                qdrant_retriever = qdrant.as_retriever(search_kwargs={"k": 7}) # Берем 7 кусков
                
                # 2. Поднимаем лексический поиск BM25 (Точные совпадения)
                target_dir = Path(data_dir_input) 
                loader = DirectoryLoader(str(target_dir), glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
                docs_for_bm25 = loader.load()
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["## Блок:", "\n\n", "\n", " "])
                chunks = text_splitter.split_documents(docs_for_bm25)
                
                # Вшиваем имя файла для надежности (как обсуждали ранее)
                for chunk in chunks:
                    file_name = Path(chunk.metadata.get('source', 'Unknown')).name
                    chunk.page_content = f"Файл_источник: {file_name}\n" + chunk.page_content
                    
                bm25_retriever = BM25Retriever.from_documents(chunks)
                bm25_retriever.k = 7 # Берем 7 кусков
                
                # 3. ГИБРИДНЫЙ ПОИСК (70% доверия точным словам, 30% смыслу)
                hybrid_retriever = EnsembleRetriever(
                    retrievers=[bm25_retriever, qdrant_retriever], 
                    weights=[0.7, 0.3] 
                )
                
                # 4. ОТКЛЮЧАЕМ FLASHRANK (Комментируем эти строки)
                # compressor = FlashrankRerank()
                # retriever = ContextualCompressionRetriever(
                #     base_compressor=compressor, 
                #     base_retriever=hybrid_retriever
                # )
                
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", sys_prompt_text),
                    ("human", "{input}"),
                ])
                
                # 5. ПЕРЕДАЕМ ЧИСТЫЙ ГИБРИД НАПРЯМУЮ
                qa_chain = create_stuff_documents_chain(llm, prompt_template)
                st.session_state['retriever'] = hybrid_retriever # <--- ИЗМЕНЕНО
                st.session_state['qa_chain'] = qa_chain
                st.session_state['system_ready'] = True
                st.success("✅ Система готова к работе!")
            except Exception as e:
                st.error(f"Ошибка запуска: {e}")

    
    if st.button("🔄 Индексировать базу", use_container_width=True):
        target_dir = Path(data_dir_input)
        if not target_dir.exists():
            st.error("Папка не найдена!")
        else:
            with st.spinner("Идет векторизация..."):
                loader = DirectoryLoader(str(target_dir), glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
                documents = loader.load()
                
                if documents:
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["## Блок:", "\n\n", "\n", " "])
                    chunks = text_splitter.split_documents(documents)
                    
                    if "e5" in embed_model_name.lower():
                        for chunk in chunks:
                            chunk.page_content = f"passage: {chunk.page_content}"
                    
                    emb_init = OpenAIEmbeddings(
                        openai_api_key=or_api_key if or_api_key else "empty",
                        openai_api_base="https://openrouter.ai/api/v1",
                        model=embed_model_name
                    )
                    Qdrant.from_documents(chunks, emb_init, url="http://localhost:6333", collection_name="mobilesmarts_knowledge", force_recreate=True, prefer_grpc=False)
                    st.success(f"Загружено {len(chunks)} блоков!")
                else:
                    st.warning("Нет файлов .md")

# --- Чат ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Спросите что-нибудь о базе MobileSmarts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not st.session_state.get('system_ready', False):
            st.warning("Сначала нажмите кнопку '🚀 ПОДКЛЮЧИТЬ ИИ' в боковой панели!")
        else:
            with st.spinner("Анализ..."):
                try:
                    search_query = f"query: {prompt}" if "e5" in embed_model_name.lower() else prompt
                    
                    retriever = st.session_state['retriever']
                    qa_chain = st.session_state['qa_chain']
                    
                    # 1. Сначала достаем документы из базы
                    docs = retriever.invoke(search_query)
                    
                    # === ДОБАВЛЯЕМ "РЕНТГЕН" В ИНТЕРФЕЙС ===
                    with st.expander("🔍 Что нашла база данных (Контекст для ИИ)"):
                        if not docs:
                            st.warning("База данных ничего не нашла по этому запросу!")
                        else:
                            for i, doc in enumerate(docs):
                                source_file = Path(doc.metadata.get('source', 'Unknown')).name
                                st.markdown(f"**Фрагмент {i+1} (из файла: `{source_file}`):**")
                                st.code(doc.page_content, language="csharp")
                    # =======================================
                    
                    # 2. Передаем документы нейросети для ответа
                    answer = qa_chain.invoke({"context": docs, "input": prompt})
                    
                    # 3. Выводим ответ
                    st.markdown(answer)
                    
                    sources = set([Path(doc.metadata.get('source', 'Unknown')).name for doc in docs])
                    if sources:
                        st.caption(f"📚 Источники: {', '.join(sources)}")
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Ошибка генерации: {e}")

# --- НАДЕЖНЫЙ ЗАПУСК ПО КНОПКЕ PLAY В IDE (ЗАЩИТА ОТ ПЕТЛИ) ---
if __name__ == "__main__":
    import os
    import sys
    import subprocess
    
    if not os.environ.get("STREAMLIT_RUNNING_FLAG"):
        print("🚀 Запускаем веб-сервер Streamlit из IDE...")
        
        current_env = os.environ.copy()
        current_env["STREAMLIT_RUNNING_FLAG"] = "true"
        current_env["PYTHONUTF8"] = "1"
        current_env["PYTHONIOENCODING"] = "utf-8"
        
        # МАГИЯ ЗДЕСЬ: Принудительно передаем дочернему процессу все пути к библиотекам (.venv)
        current_env["PYTHONPATH"] = os.pathsep.join(sys.path)
        
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", __file__], 
            env=current_env
        )
        sys.exit()