from mcp.server.fastmcp import FastMCP
import lxml.etree as ET
import os
import json
import requests
from qdrant_client import QdrantClient

# Инициализируем сервер
mcp = FastMCP("MSLX Tools")

# ==========================================
# ИНСТРУМЕНТЫ АНАЛИЗА И ЧТЕНИЯ
# ==========================================

@mcp.tool()
def extract_mslx_flow(file_path: str) -> str:
    """Парсит .mslx файл и возвращает граф переходов."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        
        actions = root.find("Actions", namespaces=nsmap) or root.find("Actions")
        if actions is None: return "Узел <Actions> не найден."
            
        flow = []
        for action in actions:
            tag = action.tag.split('}', 1)[1] if '}' in action.tag else action.tag
            name = action.attrib.get("name", "UNNAMED_NODE")
            if name == "UNNAMED_NODE" and "operationName" in action.attrib:
                name = f"Call: {action.attrib['operationName']}"
            
            node_info = {"type": tag, "name": name}
            
            for direction in ["nextDirection", "yesDirection", "noDirection", "abortDirection"]:
                if direction in action.attrib: node_info[direction] = action.attrib[direction]
                
            if "expression" in action.attrib: node_info["expression"] = action.attrib["expression"]
            if "sessionVariable" in action.attrib: node_info["sessionVariable"] = action.attrib["sessionVariable"]
                
            in_values = action.find("InValues", namespaces=nsmap) or action.find("InValues")
            if in_values is not None:
                params = [f"{v.attrib.get('name')}={v.text or ''}" for v in in_values if v.attrib.get("name")]
                if params: node_info["in_values"] = params
                
            flow.append(node_info)
            
        return json.dumps(flow, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Ошибка при парсинге: {str(e)}"

@mcp.tool()
def get_operation_summary(file_path: str) -> str:
    """Возвращает информацию о параметрах (InKeys) и возвращаемых значениях (OutKeys)."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        summary = {"name": root.attrib.get("name", "Unknown"), "parameters": [], "returns": []}
        
        for p_type in [("Parameters", "parameters"), ("Returns", "returns")]:
            node = root.find(p_type[0], namespaces=nsmap) or root.find(p_type[0])
            if node is not None:
                summary[p_type[1]] = [
                    {"name": item.attrib.get("fieldName"), "type": item.attrib.get("fieldType")}
                    for item in node
                ]
        return json.dumps(summary, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Ошибка: {str(e)}"

@mcp.tool()
def get_deep_operation_context(folder_path: str, main_file_name: str) -> str:
    """
    Глубокий анализ: Возвращает граф основной операции И сводки (Parameters/Returns) 
    по всем вложенным операциям, которые она вызывает. Вызывать ПЕРЕД редактированием.
    """
    try:
        main_file_path = os.path.join(folder_path, main_file_name)
        flow_json = extract_mslx_flow(main_file_path)
        
        if "Ошибка" in flow_json:
            return flow_json
            
        flow = json.loads(flow_json)
        context = {
            "MainOperationFlow": flow,
            "CalledOperationsSummary": {}
        }
        
        for node in flow:
            if node.get("name", "").startswith("Call:"):
                op_name = node["name"].replace("Call: ", "").strip()
                target_file = os.path.join(folder_path, f"{op_name}.mslx")
                
                if os.path.exists(target_file):
                    summary_json = get_operation_summary(target_file)
                    if "Ошибка" not in summary_json:
                        context["CalledOperationsSummary"][op_name] = json.loads(summary_json)
        
        return json.dumps(context, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Ошибка при глубоком анализе: {str(e)}"

@mcp.tool()
def find_usages(folder_path: str, operation_name: str) -> str:
    """
    Глобальный поиск зависимостей. Ищет все .mslx файлы в папке, 
    в которых вызывается указанная операция (operation_name).
    """
    try:
        usages = []
        for filename in os.listdir(folder_path):
            if not filename.endswith(".mslx"): continue
            
            file_path = os.path.join(folder_path, filename)
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                nsmap = root.nsmap
                actions = root.find("Actions", namespaces=nsmap)
                if actions is None: actions = root.find("Actions")
                if actions is None: continue
                
                for action in actions:
                    if action.attrib.get("operationName") == operation_name:
                        usages.append(filename)
                        break
            except Exception:
                continue
                
        return json.dumps({"operation": operation_name, "used_in": usages}, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Ошибка поиска зависимостей: {str(e)}"

@mcp.tool()
def get_action_code(file_path: str, action_name: str) -> str:
    """Извлекает исполняемый код (expression) или параметры вызова для узла."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        
        actions = root.find("Actions", namespaces=nsmap) or root.find("Actions")
        if actions is None: return "Узел <Actions> не найден."
            
        for action in actions:
            if action.attrib.get("name") == action_name:
                if "expression" in action.attrib: return action.attrib["expression"]
                in_values = action.find("InValues", namespaces=nsmap) or action.find("InValues")
                if in_values is not None:
                    return "\n".join([f"{v.attrib.get('name')}={v.text or ''}" for v in in_values if v.attrib.get("name")])
                return f"Код отсутствует. Атрибуты: {dict(action.attrib)}"
        return f"Узел '{action_name}' не найден."
    except Exception as e:
        return f"Ошибка: {str(e)}"

@mcp.tool()
def list_variables(file_path: str) -> str:
    """Извлекает все объявленные локальные и сессионные переменные в файле."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        variables = []
        
        params = root.find("Parameters", namespaces=nsmap)
        if params is None: params = root.find("Parameters")
        if params is not None:
            for p in params:
                variables.append({"source": "Parameter", "name": p.attrib.get("fieldName"), "type": p.attrib.get("fieldType")})
                
        actions = root.find("Actions", namespaces=nsmap)
        if actions is None: actions = root.find("Actions")
        if actions is not None:
            for action in actions.iter():
                tag = action.tag.split('}')[-1] if '}' in action.tag else action.tag
                if tag == "DeclareAction":
                    variables.append({"source": "DeclareAction", "name": action.attrib.get("fieldName"), "type": action.attrib.get("fieldType")})
                elif tag in ("SelectDocumentLineAction", "SelectDocumentLinesAction"):
                     var_name = action.attrib.get("sessionVariable")
                     if var_name:
                         variables.append({"source": "DB Select (Session)", "name": var_name, "type": "Object/List"})
                         
        return json.dumps(variables, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Ошибка при поиске переменных: {str(e)}"

@mcp.tool()
def index_configuration(folder_path: str) -> str:
    """Vector Indexer: Сканирует папку и собирает массив всех операций и их параметров."""
    try:
        index = []
        for filename in os.listdir(folder_path):
            if not filename.endswith(".mslx"): continue
            file_path = os.path.join(folder_path, filename)
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                nsmap = root.nsmap
                
                op_name = root.attrib.get("name", filename)
                params = []
                p_node = root.find("Parameters", namespaces=nsmap)
                if p_node is None: p_node = root.find("Parameters")
                if p_node is not None:
                    params = [p.attrib.get("fieldName") for p in p_node if p.attrib.get("fieldName")]
                    
                index.append({"file": filename, "operation_name": op_name, "parameters": params})
            except Exception:
                continue
        return json.dumps(index, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Ошибка индексации: {str(e)}"

@mcp.tool()
def read_global_fields(folder_path: str) -> str:
    """Извлекает информацию о полях из глобальных файлов конфигурации (.xml)."""
    try:
        fields_info = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".xml") and ("Fields" in filename or "Warehouse" in filename):
                file_path = os.path.join(folder_path, filename)
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    nsmap = root.nsmap
                    
                    for field in root.xpath('//Field | //FieldInfo', namespaces=nsmap):
                        name = field.attrib.get("name") or field.attrib.get("fieldName")
                        ftype = field.attrib.get("type") or field.attrib.get("fieldType")
                        if name: fields_info.append({"file": filename, "name": name, "type": ftype})
                except Exception:
                    continue
        return json.dumps(fields_info, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Ошибка при извлечении полей конфигурации: {str(e)}"

# ==========================================
# ИНСТРУМЕНТЫ РЕДАКТИРОВАНИЯ
# ==========================================

@mcp.tool()
def update_action_code(file_path: str, action_name: str, new_code: str) -> str:
    """Заменяет код в атрибуте expression указанного узла и сохраняет файл."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        
        actions = root.find("Actions", namespaces=nsmap)
        if actions is None: actions = root.find("Actions")
        if actions is None: return "Узел <Actions> не найден."
            
        for action in actions:
            if action.attrib.get("name") == action_name:
                if "expression" in action.attrib:
                    action.attrib["expression"] = new_code
                    tree.write(file_path, encoding="utf-8", xml_declaration=True)
                    return f"Успешно обновлен код в узле '{action_name}' файла {os.path.basename(file_path)}."
                else:
                    return f"У узла '{action_name}' нет атрибута 'expression'."
                    
        return f"Узел '{action_name}' не найден."
    except Exception as e:
        return f"Ошибка при обновлении: {str(e)}"

@mcp.tool()
def update_in_values(file_path: str, action_name: str, updates_json: str) -> str:
    """
    Обновляет или добавляет параметры в блоке InValues.
    updates_json - это JSON-строка со словарем {имя_параметра: новое_значение}.
    """
    try:
        updates = json.loads(updates_json)
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        
        actions = root.find("Actions", namespaces=nsmap)
        if actions is None: actions = root.find("Actions")
        if actions is None: return "Узел <Actions> не найден."
            
        for action in actions:
            if action.attrib.get("name") == action_name:
                in_values = action.find("InValues", namespaces=nsmap)
                if in_values is None: in_values = action.find("InValues")
                
                # Если InValues вообще нет, создаем его
                if in_values is None:
                    namespace = nsmap.get(None, "")
                    tag = f"{{{namespace}}}InValues" if namespace else "InValues"
                    in_values = ET.SubElement(action, tag)

                # Обновляем существующие или добавляем новые
                for key, val_str in updates.items():
                    found = False
                    for val_node in in_values:
                        if val_node.attrib.get("name") == key:
                            val_node.text = str(val_str)
                            found = True
                            break
                    if not found:
                        namespace = nsmap.get(None, "")
                        tag = f"{{{namespace}}}Value" if namespace else "Value"
                        new_val = ET.SubElement(in_values, tag, name=key)
                        new_val.text = str(val_str)
                
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                return f"Успешно обновлены InValues в узле '{action_name}'."
                
        return f"Узел '{action_name}' не найден."
    except Exception as e:
        return f"Ошибка при обновлении InValues: {str(e)}"

@mcp.tool()
def add_action_node(file_path: str, action_type: str, action_name: str, next_direction: str, additional_attributes_json: str = "{}") -> str:
    """
    Добавляет новый узел в конец списка Actions.
    action_type - например, AssignAction, OperationAction.
    additional_attributes_json - JSON-строка с атрибутами (например: '{"expression": "1+1"}').
    """
    try:
        attrs = json.loads(additional_attributes_json)
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        
        actions = root.find("Actions", namespaces=nsmap)
        if actions is None: actions = root.find("Actions")
        if actions is None: return "Узел <Actions> не найден."
        
        namespace = nsmap.get(None, "")
        tag = f"{{{namespace}}}{action_type}" if namespace else action_type
        
        new_action = ET.SubElement(actions, tag)
        new_action.set("name", action_name)
        new_action.set("nextDirection", next_direction)
        
        for k, v in attrs.items():
            new_action.set(k, str(v))
            
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        return f"Узел '{action_name}' типа {action_type} успешно добавлен."
    except Exception as e:
        return f"Ошибка при добавлении узла: {str(e)}"

@mcp.tool()
def delete_action_node(file_path: str, action_name: str) -> str:
    """Удаляет узел с указанным именем из блока Actions."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        
        actions = root.find("Actions", namespaces=nsmap)
        if actions is None: actions = root.find("Actions")
        if actions is None: return "Узел <Actions> не найден."
        
        for action in actions:
            if action.attrib.get("name") == action_name:
                actions.remove(action)
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                return f"Узел '{action_name}' успешно удален."
                
        return f"Узел '{action_name}' не найден."
    except Exception as e:
        return f"Ошибка при удалении узла: {str(e)}"


@mcp.tool()
def save_sdd_doc(folder_path: str, document_name: str, content: str) -> str:
    """
    Сохраняет техническую спецификацию (SDD) в формате Markdown (.md).
    Автоматически создает папку Docs внутри указанного пути, если ее нет.
    folder_path - корневой путь (обычно путь к /Document).
    document_name - имя файла (например, 'ds_CheckBarcode_SDD.md').
    content - текст спецификации в формате Markdown.
    """
    try:
        # Папка Docs будет лежать рядом с DocumentTypes и Operations
        docs_dir = os.path.join(folder_path, "Docs")
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
        
        # Обеспечиваем правильное расширение
        if not document_name.endswith(".md"):
            document_name += ".md"
            
        file_path = os.path.join(docs_dir, document_name)
        
        # Записываем контент
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Спецификация (SDD) успешно сохранена в: {os.path.abspath(file_path)}"
    except Exception as e:
        return f"Ошибка при сохранении SDD: {str(e)}"


@mcp.tool()
def update_node_attributes(file_path: str, action_name: str, attributes_json: str) -> str:
    """Универсальный инструмент для изменения ЛЮБЫХ атрибутов узла."""
    try:
        updates = json.loads(attributes_json)
        tree = ET.parse(file_path)
        root = tree.getroot()
        nsmap = root.nsmap
        
        actions = root.find("Actions", namespaces=nsmap) or root.find("Actions")
        if actions is None: return "Узел <Actions> не найден."
            
        for action in actions:
            if action.attrib.get("name") == action_name:
                for key, value in updates.items():
                    action.set(key, str(value))
                tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
                return f"Успешно обновлены атрибуты узла '{action_name}'."
        return f"Узел '{action_name}' не найден."
    except Exception as e:
        return f"Ошибка: {str(e)}"
    
@mcp.tool()
def semantic_search_syntax(query: str, n_results: int) -> str:
    """
    RAG-поиск: Ищет информацию и примеры кода в базе знаний MobileSmarts (Qdrant).
    ВАЖНО: Параметр query должен быть кратким поисковым запросом.
    """
    try:
        import os
        import requests
        import json
        from qdrant_client import QdrantClient
        
        safe_query = query[:1000]
        
        # === БЛОК НАСТРОЕК ВЕКТОРИЗАЦИИ (OpenRouter) ===
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "") 
        # ===============================================

        if OPENROUTER_API_KEY:
            # --- Облачный API OpenRouter (Быстро, не жрет память) ---
            api_url = "https://openrouter.ai/api/v1/embeddings"
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "baai/bge-m3",
                "input": safe_query
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=15)
            
            if response.status_code != 200:
                return f"Ошибка OpenRouter API: {response.text}"
                
            # Извлекаем вектор из ответа в стиле OpenAI
            query_vector = response.json().get("data", [])[0].get("embedding")
            
        else:
            # --- Fallback: Локальная Ollama (Если ключа нет) ---
            embed_model = "bge-m3" 
            ollama_url = "http://localhost:11434/api/embeddings"
            
            response = requests.post(
                ollama_url, 
                json={"model": embed_model, "prompt": safe_query}, 
                timeout=15
            )
            
            if response.status_code != 200:
                return f"Ошибка локальной Ollama: {response.text}"
                
            query_vector = response.json().get("embedding")

        # Проверка, что вектор успешно получен
        if not query_vector:
            return "Ошибка: Модель вернула пустой вектор."

        # === ПОИСК В БАЗЕ QDRANT ===
        client = QdrantClient(url="http://localhost:6333")
        
        # ИСПОЛЬЗУЕМ НОВЫЙ МЕТОД query_points (вместо устаревшего search)
        search_response = client.query_points(
            collection_name="mobilesmarts_knowledge",
            query=query_vector,
            limit=int(n_results)
        )
        
        # Проверяем свойство .points
        if not search_response.points:
            return f"Ничего не найдено по запросу: '{safe_query}'."
            
        formatted_results = []
        # Перебираем массив .points
        for hit in search_response.points:
            content = hit.payload.get("page_content", "")
            metadata = hit.payload.get("metadata", {})
            source_path = metadata.get("source", "Unknown")
            source_name = source_path.replace("\\", "/").split("/")[-1]
            
            formatted_results.append({
                "source_file": source_name,
                "relevance_score": round(hit.score, 3),
                "content": content
            })
            
        return json.dumps(formatted_results, indent=2, ensure_ascii=False)
        
    except requests.exceptions.Timeout:
        return "Ошибка: Превышено время ожидания векторизатора."
    except Exception as e:
        return f"Критическая ошибка RAG-инструмента: {str(e)}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MSLX MCP Server")
    parser.add_argument("--transport", type=str, default="stdio", choices=["stdio", "sse", "streamable-http"], help="Транспортный протокол")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Хост для HTTP сервера")
    parser.add_argument("--port", type=int, default=8000, help="Порт для HTTP сервера")
    
    args = parser.parse_args()
    
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    
    if args.transport != "stdio":
        print(f"Запуск MCP сервера на http://{args.host}:{args.port}")
        if args.transport == "streamable-http":
            print(f"URL: http://{args.host}:{args.port}/mcp")
        elif args.transport == "sse":
             print(f"URL: http://{args.host}:{args.port}/sse")
    print("⏳ Инициализация инструментов MSLX Tools...")         
    mcp.run(transport=args.transport)