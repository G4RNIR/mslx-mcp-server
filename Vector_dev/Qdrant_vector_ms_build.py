import os
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

def setup_and_run_rag():
    # 1. Запрашиваем путь к данным
    user_input_dir = input("Введите путь к директории с документацией (.md, .txt): ").strip()
    user_input_dir = user_input_dir.strip('"').strip("'")
    target_dir = Path(user_input_dir)

    if not target_dir.exists() or not target_dir.is_dir():
        print("Указанная директория не найдена!")
        return

    # 2. Загрузка данных
    print(f"\nЗагрузка текстовых документов из {target_dir}...")
    loader = DirectoryLoader(str(target_dir), glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("Документы (.md) не найдены. Сначала запустите парсер!")
        return
        
    print(f"Загружено документов: {len(documents)}")

    # 3. Чанкинг
    print("Разбиение документов на смысловые блоки...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n## Блок:", "\n\n", "\n", " "] 
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Создано чанков: {len(chunks)}")

    # 4. Embeddings
    print("Загрузка embedding-модели (multilingual-e5-large)...")
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

    # 5. Загрузка в векторную БД
    print("Отправка векторов в Qdrant (Docker)...")
    qdrant = Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        url="http://localhost:6333", # Подключение к Docker
        collection_name="mobilesmarts_knowledge",
        prefer_grpc=False
    )

    base_retriever = qdrant.as_retriever(search_kwargs={"k": 20})

    # 6. Reranking
    print("Настройка системы фильтрации (Flashrank)...")
    compressor = FlashrankRerank(top_n=5)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=base_retriever
    )

    # 7. LLM Настройка
    llm = ChatOpenAI(
        model="llama-3-8b-instruct", # Замените на вашу модель (или gpt-4o-mini)
        base_url="https://api.openai.com/v1", # Замените на эндпоинт вашего API
        api_key="your_api_key_here",
        temperature=0.1
    )

    system_prompt = (
        "Ты — эксперт по платформе MobileSmarts (Cleverence). "
        "Используй контекст ниже для ответа на вопрос. "
        "Если ответа нет в контексте, честно скажи об этом.\n\n"
        "Контекст:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(compression_retriever, question_answer_chain)

    # 8. Интерактивный чат
    print("\nСистема готова! Напишите 'выход' или 'exit' для завершения.")
    while True:
        question = input("\nВаш вопрос по базе MobileSmarts: ").strip()
        if question.lower() in ['выход', 'exit', 'quit']:
            break
        if not question:
            continue
            
        print("Думаю...")
        try:
            response = rag_chain.invoke({"input": question})
            print(f"\n💡 Ответ:\n{response['answer']}")
            print("\n📚 Источники:")
            
            # Оставляем только уникальные источники для красоты вывода
            sources = set([doc.metadata.get('source', 'Unknown') for doc in response["context"]])
            for source in sources:
                print(f"- {Path(source).name}")
        except Exception as e:
            print(f"Произошла ошибка при генерации ответа: {e}")

if __name__ == "__main__":
    setup_and_run_rag()