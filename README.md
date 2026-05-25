# MSLX Tools

MCP-сервер и RAG-пайплайн для анализа, трассировки и безопасного редактирования конфигураций Mobile SMARTS / Cleverence.

Проект решает две основные задачи:

- дает AI-клиенту набор MCP-инструментов для чтения и изменения `.mslx` XML-деревьев;
- собирает локальную базу знаний по Mobile SMARTS в Qdrant и позволяет искать синтаксис/примеры через RAG.

## Структура проекта

```text
mslx-mcp-server/
  server.py                         # MCP-сервер MSLX Tools
  MobileSmartsSyntaxChecker/        # CLI-checker синтаксиса через Cleverence.Parsing.dll
    Program.cs
    build.ps1
  SystemPrompt.md                   # системный промпт для AI-агента
  RAG_System_prompt.md              # системный промпт для web RAG-чата
  setup.bat                         # быстрый старт Windows
  docker-compose.yml                # Qdrant
  requirements.txt                  # Python-зависимости
  generate_ms_dictionary.py         # генератор словаря синтаксиса Mobile SMARTS
  test_search.py                    # проверка поиска Qdrant
  test_hybrid.py                    # проверка гибридного поиска
  Vector_dev/
    web_rag.py                      # Streamlit UI для индексации и чата
    mslx_cleaning_for_RAG.py        # конвертация .mslx в Markdown для RAG
    Qdrant_vector_ms_build.py       # отдельный скрипт загрузки в Qdrant
    Official_Docs/                  # markdown-документация Cleverence
```

Рабочая конфигурация Mobile SMARTS не хранится в этом репозитории. Для MCP-инструментов передавайте абсолютный путь к папке `Document` нужной базы, например:

```text
C:\Cleverence\Databases\MyBase\Document
```

Внутри `Document` сервер ожидает стандартные папки:

- `DocumentTypes/`
- `Operations/`
- `Docs/`

## Требования

- Windows 10/11.
- Python 3.10+.
- Docker Desktop для Qdrant.
- Git.
- Доступ к OpenRouter API, если используется облачная векторизация/LLM.
- Опционально: локальная Ollama для fallback-режима RAG.
- Локальный `MobileSmartsSyntaxChecker.exe` на базе `Cleverence.Parsing.dll`.

Исходники checker-а лежат в `MobileSmartsSyntaxChecker/`. `setup.bat` собирает его автоматически в:

```text
MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe
```

Путь к syntax checker задается переменной:

```env
MOBILESMARTS_SYNTAX_CHECKER=E:\mcp-ms\mslx-mcp-server\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe
MOBILESMARTS_DIR=E:\MobileSmarts\Desktop
```

Если checker не найден, инструмент `validate_mslx_syntax` вернет понятную ошибку и заблокирует pre-flight проверки выражений.

## Быстрое развертывание

1. Клонируйте репозиторий:

```powershell
git clone <repo-url> E:\mcp-ms\mslx-mcp-server
cd E:\mcp-ms\mslx-mcp-server
```

2. Запустите Docker Desktop.

3. Выполните установку:

```powershell
.\setup.bat
```

Скрипт:

- поднимет Qdrant через `docker-compose up -d`;
- создаст `.venv`;
- установит зависимости из `requirements.txt`;
- создаст `.env` из `.env.example`, если `.env` отсутствует.

4. Заполните `.env`:

```env
OPENROUTER_API_KEY=sk-or-v1-...
MOBILESMARTS_SYNTAX_CHECKER=E:\mcp-ms\mslx-mcp-server\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe
MOBILESMARTS_DIR=E:\MobileSmarts\Desktop
```

Не коммитьте `.env`.

## Ручное развертывание

Если `setup.bat` не подходит:

```powershell
docker-compose up -d
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Проверка Python-части:

```powershell
.\.venv\Scripts\python.exe -m py_compile server.py
```

Проверка Qdrant:

```powershell
curl http://localhost:6333/collections
```

## Запуск MCP-сервера

### Stdio

Основной режим для Cursor, Cline, Roo Code и других локальных AI-клиентов:

```powershell
.\.venv\Scripts\python.exe server.py --transport stdio
```

Пример конфигурации MCP-клиента:

```json
{
  "mcpServers": {
    "MSLX Tools": {
      "command": "E:\\mcp-ms\\mslx-mcp-server\\.venv\\Scripts\\python.exe",
      "args": [
        "E:\\mcp-ms\\mslx-mcp-server\\server.py",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### HTTP/SSE

Для отладки:

```powershell
.\.venv\Scripts\python.exe server.py --transport streamable-http --host 127.0.0.1 --port 8000
```

URL:

```text
http://127.0.0.1:8000/mcp
```

SSE:

```powershell
.\.venv\Scripts\python.exe server.py --transport sse --host 127.0.0.1 --port 8000
```

URL:

```text
http://127.0.0.1:8000/sse
```

## MCP-инструменты

Все пути передаются абсолютными. Параметры с суффиксом `_json` передаются строкой с валидным JSON, а не объектом.

### Чтение и анализ

| Инструмент | Назначение |
|---|---|
| `extract_mslx_flow(file_path)` | Возвращает плоский граф действий из блока `Actions`. |
| `get_operation_summary(file_path)` | Возвращает параметры и возвращаемые значения операции. |
| `get_deep_operation_context(folder_path, main_file_name)` | Возвращает граф основной операции и сводки вложенных операций. |
| `find_usages(folder_path, operation_name, include_document_types=true)` | Ищет вызовы операции в `Operations` и, при необходимости, в `DocumentTypes`. Пустой `used_in` считается блокером перед редактированием. |
| `trace_document_entrypoint(document_root_path, document_type_name, max_depth=10)` | Строит цепочку от типа документа к вызываемым операциям. |
| `trace_operation_calls(file_path, depth=5, document_root_path="")` | Рекурсивно раскрывает все `OperationAction`. |
| `find_reachable_actions(document_root_path, document_type_name, action_type, max_depth=10)` | Ищет достижимые действия заданного типа из точки входа документа. |
| `explain_call_path_to_action(document_root_path, document_type_name, target_action_type_or_name, max_depth=10)` | Объясняет путь от документа до действия по типу или имени. |
| `get_action_code(file_path, action_name)` | Возвращает `expression` или параметры вызова конкретного узла. |
| `list_variables(file_path)` | Возвращает объявленные параметры, локальные и сессионные переменные. |
| `index_configuration(folder_path)` | Индексирует операции и их параметры в папке. |
| `read_global_fields(folder_path)` | Читает глобальные поля из XML-конфигурации. |
| `semantic_search_syntax(query, n_results, source_type="all")` | Ищет синтаксис и примеры в Qdrant. `source_type`: `all`, `code`, `official`. |

### Проверка и редактирование

| Инструмент | Назначение |
|---|---|
| `validate_mslx_syntax(source, mode="expression", normalize_braces=true)` | Проверяет синтаксис через Cleverence parser. Русские идентификаторы передаются в checker безопасно через JSON escape. |
| `copy_operation_file(source_file_path, target_file_path, new_operation_name="", overwrite=false)` | Копирует `.mslx` операцию и меняет корневой `name`. |
| `update_operation_root_attributes(file_path, attributes_json)` | Меняет атрибуты корневого узла операции или типа документа. |
| `add_document_type_column(file_path, column_name, attributes_json="{}")` | Добавляет колонку в `DocumentType/Columns`. |
| `update_comparing_field_names_for_current_items(file_path, action_name, field_names_json, mode="merge", item_tag="")` | Обновляет вложенный список `ComparingFieldNamesForCurrentItems` у `AcceptInDocumentAction`. |
| `update_operation_action_io(file_path, action_name, in_keys_json="[]", out_keys_json="[]", out_values_json="[]", mode="merge")` | Создает или обновляет `InKeys`, `OutKeys`, `OutValues` внутри `OperationAction`. |
| `update_action_code(file_path, action_name, new_code)` | Меняет атрибут `expression` узла с pre-flight проверкой. |
| `update_in_values(file_path, action_name, updates_json)` | Обновляет/добавляет `InValues`. |
| `add_action_node(file_path, action_type, action_name, next_direction, additional_attributes_json="{}")` | Добавляет действие в конец `Actions`. |
| `delete_action_node(file_path, action_name)` | Удаляет действие из `Actions`. |
| `update_node_attributes(file_path, action_name, attributes_json)` | Меняет любые атрибуты действия. |
| `save_sdd_doc(folder_path, document_name, content)` | Сохраняет SDD в `Document/Docs`. |

### Примеры вызовов

Проверить реальный путь от документа до записи товара:

```json
{
  "document_root_path": "C:\\Base\\Document",
  "document_type_name": "Отгрузка",
  "target_action_type_or_name": "AcceptInDocumentAction",
  "max_depth": 10
}
```

Добавить поле в список сравнения строк:

```json
{
  "file_path": "C:\\Base\\Document\\Operations\\ОснПроцесс.mslx",
  "action_name": "Запись SelectedProduct в документ",
  "field_names_json": "[\"Номенклатура\", \"Характеристика\", \"ds_BoxId\"]",
  "mode": "merge",
  "item_tag": ""
}
```

Скопировать глобальную операцию перед доработкой:

```json
{
  "source_file_path": "C:\\Base\\Document\\Operations\\ЗаписьТовара.mslx",
  "target_file_path": "C:\\Base\\Document\\Operations\\ds_ЗаписьТовара.mslx",
  "new_operation_name": "ds_ЗаписьТовара",
  "overwrite": false
}
```

## Обязательный workflow редактирования `.mslx`

1. Найти точку входа документа через `trace_document_entrypoint`.
2. Построить reachability-граф через `trace_operation_calls`, `find_reachable_actions` или `explain_call_path_to_action`.
3. Проверить зависимости через `find_usages`.
4. Если `find_usages.used_in=[]` или действие не достижимо из документа, не редактировать операцию.
5. Для глобальной операции сначала сделать копию через `copy_operation_file`, затем заменить вызовы на `ds_`-операцию.
6. Проверить выражения через `validate_mslx_syntax`.
7. Внести изменения только MCP-инструментами.
8. Сохранить SDD через `save_sdd_doc`.
9. Проверить `git diff`.

## RAG-пайплайн

### 1. Подготовить Markdown из `.mslx`

Скрипт `Vector_dev/mslx_cleaning_for_RAG.py` рекурсивно читает `.mslx` и сохраняет Markdown в подпапку `Cleaned_Markdown`.

Интерактивный запуск:

```powershell
.\.venv\Scripts\python.exe Vector_dev\mslx_cleaning_for_RAG.py
```

Запуск с аргументом:

```powershell
.\.venv\Scripts\python.exe Vector_dev\mslx_cleaning_for_RAG.py "C:\Base\Document"
```

### 2. Сгенерировать словарь синтаксиса

```powershell
.\.venv\Scripts\python.exe generate_ms_dictionary.py --folder "C:\Base\Document\Cleaned_Markdown" --output "C:\Base\Document\Docs\_Syntax_Dictionary.md"
```

Если запустить без аргументов, скрипт предложит выбрать папку через диалог.

### 3. Запустить Qdrant

```powershell
docker-compose up -d
```

Коллекция, которую использует проект:

```text
mobilesmarts_knowledge
```

### 4. Запустить Streamlit UI

```powershell
.\.venv\Scripts\python.exe Vector_dev\web_rag.py
```

Скрипт сам перезапустится через:

```powershell
python -m streamlit run Vector_dev\web_rag.py
```

В UI:

1. Укажите `OPENROUTER_API_KEY`.
2. Укажите папку с кодом в Markdown, например `C:\Base\Document\Cleaned_Markdown`.
3. Укажите папку официальной документации, например `E:\mcp-ms\mslx-mcp-server\Vector_dev\Official_Docs`.
4. Нажмите `Индексировать базу`.
5. Нажмите `Подключить ИИ`.

## Проверка поиска

После индексации:

```powershell
.\.venv\Scripts\python.exe test_search.py
.\.venv\Scripts\python.exe test_hybrid.py
```

Также можно проверить MCP-инструмент:

```json
{
  "query": "как обратиться к полю строки документа с русским именем",
  "n_results": 5,
  "source_type": "all"
}
```

## Частые проблемы

### `Mobile SMARTS syntax checker not found`

Соберите локальный checker:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\MobileSmartsSyntaxChecker\build.ps1
```

Проверьте `MOBILESMARTS_SYNTAX_CHECKER` в `.env`.

Если checker собран, но не находит `Cleverence.Parsing.dll`, проверьте `MOBILESMARTS_DIR`. Это должна быть папка Mobile SMARTS, где лежит `Cleverence.Parsing.dll`, например:

```text
E:\MobileSmarts\Desktop
```

### `setup.bat` не создает `.env`

Убедитесь, что в репозитории есть `.env.example`. Если нет, создайте `.env` вручную:

```env
OPENROUTER_API_KEY=
MOBILESMARTS_SYNTAX_CHECKER=E:\mcp-ms\mslx-mcp-server\MobileSmartsSyntaxChecker\bin\MobileSmartsSyntaxChecker.exe
MOBILESMARTS_DIR=E:\MobileSmarts\Desktop
```

### Qdrant не отвечает

```powershell
docker ps
docker-compose up -d
curl http://localhost:6333/collections
```

### RAG ничего не находит

Проверьте:

- Qdrant запущен;
- коллекция `mobilesmarts_knowledge` создана;
- в UI нажата кнопка `Индексировать базу`;
- пути к `Cleaned_Markdown` и `Official_Docs` существуют;
- `OPENROUTER_API_KEY` корректен.

### Русские поля падают в `validate_mslx_syntax`

В актуальной версии `server.py` payload в checker отправляется как ASCII JSON с `\uXXXX`, поэтому выражения вида `item.номер` и `SelectedLine.номер` проходят синтаксическую проверку. Если ошибка повторяется, проверьте, что MCP-клиент запущен именно из обновленного репозитория.

## Правила безопасности для доработок

- Не редактировать глобальную операцию напрямую: сначала копия с префиксом `ds_`.
- Не выбирать операцию по имени: сначала reachability-граф от типа документа.
- Пустой `find_usages` — блокер.
- Новые переменные, параметры и узлы начинать с `ds_`.
- Нетиповой код маркировать в атрибуте `comment`: `Нетиповой код ds++ <дата>`.
- Не писать комментарии внутри `expression`.
- Не использовать C#-циклы внутри `expression`; использовать XML-узлы процесса.
- Перед записью выражений сверяться со словарем синтаксиса и `validate_mslx_syntax`.

## Команды для разработчика

```powershell
.\.venv\Scripts\python.exe -m py_compile server.py
git status --short
git diff -- server.py SystemPrompt.md README.md
```

Для запуска MCP Inspector используйте режим HTTP или SSE и подключайтесь к локальному URL.
