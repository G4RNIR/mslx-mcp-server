import json
# ВАЖНО: Замените "mcp_server" на то имя файла, где у вас лежит код сервера (без .py)
from server import semantic_search_syntax 

def test_my_rag():
    # Наш тестовый запрос
    test_query = "как работать с табличной частью документа, добавление строк, схлопывание по ключевым полям"
    print(f"🔍 Запускаем поиск по запросу: '{test_query}'\n")
    print("⏳ Ждем ответ от Ollama и Qdrant...\n")

    # Вызываем функцию точно так же, как это сделал бы ИИ
    result_string = semantic_search_syntax(test_query, n_results=3)

    # Пытаемся красиво вывести JSON
    try:
        # Если вернулся правильный JSON с результатами
        parsed_data = json.loads(result_string)
        print("✅ УСПЕХ! Вот что нашла база данных:")
        print(json.dumps(parsed_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        # Если вернулась строка с ошибкой (например "Ошибка локальной модели...")
        print("❌ ПРОИЗОШЛА ОШИБКА В ФУНКЦИИ:")
        print(result_string)

if __name__ == "__main__":
    test_my_rag()