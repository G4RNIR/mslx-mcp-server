from mcp.server.fastmcp import FastMCP
import lxml.etree as ET
import os
import json
import subprocess
import shutil
import requests
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()


# Инициализируем сервер
mcp = FastMCP("MSLX Tools")

MOBILESMARTS_SYNTAX_CHECKER = os.getenv(
    "MOBILESMARTS_SYNTAX_CHECKER",
    os.path.join(os.path.dirname(__file__), "MobileSmartsSyntaxChecker", "bin", "MobileSmartsSyntaxChecker.exe"),
)

EXPRESSION_ATTRIBUTE_NAMES = {
    "expression",
    "declaredexpression",
    "whereexpression",
    "sourcevalue",
    "targetvalue",
    "items",
}


def _json_response(payload: dict) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _run_syntax_checker(mode: str, source: str, normalize_braces: bool = True) -> dict:
    checker_path = os.getenv("MOBILESMARTS_SYNTAX_CHECKER", MOBILESMARTS_SYNTAX_CHECKER)
    if not os.path.exists(checker_path):
        return {
            "Ok": False,
            "Mode": mode,
            "Source": source,
            "Errors": [
                f"Mobile SMARTS syntax checker not found: {checker_path}. "
                "Build it with .\\MobileSmartsSyntaxChecker\\build.ps1 "
                "or set MOBILESMARTS_SYNTAX_CHECKER."
            ],
        }

    payload = {
        "mode": mode,
        "source": "" if source is None else str(source),
        "normalizeBraces": normalize_braces,
    }
    mobile_smarts_dir = os.getenv("MOBILESMARTS_DIR", "").strip()
    if mobile_smarts_dir:
        payload["mobileSmartsDir"] = mobile_smarts_dir
    try:
        completed = subprocess.run(
            [checker_path, "--stdin"],
            input=json.dumps(payload, ensure_ascii=True),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
    except Exception as exc:
        return {
            "Ok": False,
            "Mode": mode,
            "Source": source,
            "Errors": [f"Failed to run Mobile SMARTS syntax checker: {exc}"],
        }

    try:
        result = json.loads(completed.stdout) if completed.stdout.strip() else {}
    except json.JSONDecodeError:
        result = {
            "Ok": False,
            "Mode": mode,
            "Source": source,
            "Errors": ["Syntax checker returned non-JSON output."],
            "stdout": completed.stdout,
        }

    result.setdefault("Ok", completed.returncode == 0)
    result.setdefault("Mode", mode)
    result.setdefault("Source", source)
    result["exit_code"] = completed.returncode
    if completed.stderr.strip():
        result["stderr"] = completed.stderr.strip()
    if completed.returncode != 0 and not result.get("Errors"):
        result["Errors"] = [completed.stderr.strip() or "Syntax checker failed."]
    return result


def _syntax_error_response(context: str, checker_result: dict) -> str:
    return _json_response(
        {
            "ok": False,
            "blocked": True,
            "context": context,
            "message": "Запись заблокирована: Mobile SMARTS syntax checker вернул ошибку.",
            "checker": checker_result,
        }
    )


def _validate_or_error(mode: str, source: str, context: str, normalize_braces: bool = True):
    result = _run_syntax_checker(mode, source, normalize_braces)
    if result.get("Ok") is True or result.get("ok") is True:
        return None
    return _syntax_error_response(context, result)


def _syntax_mode_for_attribute(attribute_name: str):
    normalized = attribute_name.replace("_", "").replace("-", "").lower()
    if normalized in EXPRESSION_ATTRIBUTE_NAMES:
        return "expression"
    return None


def _local_name(node_or_tag) -> str:
    tag = node_or_tag.tag if hasattr(node_or_tag, "tag") else str(node_or_tag)
    return tag.split("}", 1)[1] if "}" in tag else tag


def _namespace(root) -> str:
    return root.nsmap.get(None, "") if root.nsmap else ""


def _tag(root, local_name: str) -> str:
    namespace = _namespace(root)
    return f"{{{namespace}}}{local_name}" if namespace else local_name


def _find_child(parent, local_name: str):
    for child in parent:
        if _local_name(child) == local_name:
            return child
    return None


def _find_action(root, action_name: str):
    actions = _find_child(root, "Actions")
    if actions is None:
        return None
    for action in actions.iter():
        if action.attrib.get("name") == action_name:
            return action
    return None


def _load_json_object(raw: str, context: str) -> dict:
    value = json.loads(raw or "{}")
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be a JSON object string.")
    return value


def _load_io_items(raw: str, context: str) -> list:
    value = json.loads(raw or "[]")
    if isinstance(value, dict) and isinstance(value.get("items"), list):
        value = value["items"]
    elif isinstance(value, dict):
        mapped_items = []
        for key, item in value.items():
            if not isinstance(item, dict):
                mapped_items.append({"name": key, "text": item})
                continue
            mapped_item = dict(item)
            if isinstance(mapped_item.get("attributes"), dict):
                mapped_item["attributes"] = dict(mapped_item["attributes"])
                mapped_item["attributes"].setdefault("name", key)
            else:
                mapped_item.setdefault("name", key)
            mapped_items.append(mapped_item)
        value = mapped_items
    if not isinstance(value, list):
        raise ValueError(f"{context} must be a JSON array string, object map, or object with items array.")
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"Every item in {context} must be an object.")
    return value


def _load_string_items(raw: str, context: str) -> list:
    value = json.loads(raw or "[]")
    if isinstance(value, dict) and isinstance(value.get("items"), list):
        value = value["items"]
    elif isinstance(value, dict):
        value = list(value.values())
    if not isinstance(value, list):
        raise ValueError(f"{context} must be a JSON array string, object map, or object with items array.")

    result = []
    for item in value:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            field_name = item.get("name") or item.get("fieldName") or item.get("value") or item.get("text")
            if field_name is None:
                raise ValueError(f"Every object in {context} must contain name, fieldName, value, or text.")
            result.append(str(field_name))
        else:
            raise ValueError(f"Every item in {context} must be a string or object.")
    return result


def _item_identity(item: dict):
    attrs = item.get("attributes") if isinstance(item.get("attributes"), dict) else item
    for key in ("name", "fieldName", "key", "id"):
        if attrs.get(key) is not None:
            return key, str(attrs.get(key))
    return None, None


def _node_identity(node):
    for key in ("name", "fieldName", "key", "id"):
        if node.attrib.get(key) is not None:
            return key, node.attrib.get(key)
    return None, None


def _node_string_value(node) -> str:
    for key in ("name", "fieldName", "value"):
        if node.attrib.get(key) is not None:
            return node.attrib.get(key)
    return (node.text or "").strip()


def _apply_item_to_node(node, item: dict, context: str):
    attrs = item.get("attributes") if isinstance(item.get("attributes"), dict) else {
        key: value
        for key, value in item.items()
        if key not in ("tag", "text", "children", "attributes")
    }
    for key, value in attrs.items():
        mode = _syntax_mode_for_attribute(key)
        if mode:
            syntax_error = _validate_or_error(mode, str(value), f"{context}.{key}")
            if syntax_error:
                return syntax_error
        node.set(key, str(value))
    if "text" in item:
        text = "" if item["text"] is None else str(item["text"])
        syntax_error = _validate_or_error("auto", text, f"{context}.text")
        if syntax_error:
            return syntax_error
        node.text = text
    if isinstance(item.get("children"), list):
        for existing_child in list(node):
            node.remove(existing_child)
        for child_item in item["children"]:
            if not isinstance(child_item, dict):
                return _json_response({"ok": False, "error": f"{context}.children item must be an object."})
            child_tag = child_item.get("tag", "Value")
            child = ET.SubElement(node, _tag(node.getroottree().getroot(), child_tag))
            syntax_error = _apply_item_to_node(child, child_item, f"{context}.{child_tag}")
            if syntax_error:
                return syntax_error
    return None


def _upsert_block_items(root, action, block_name: str, raw_json: str, default_item_tag: str, mode: str):
    items = _load_io_items(raw_json, block_name)
    if not items:
        return 0, 0
    block = _find_child(action, block_name)
    if block is None:
        block = ET.SubElement(action, _tag(root, block_name))
    if mode == "replace":
        for child in list(block):
            block.remove(child)
    if mode not in ("merge", "replace"):
        raise ValueError("mode must be 'merge' or 'replace'.")

    updated = 0
    added = 0
    for index, item in enumerate(items):
        item_tag = item.get("tag") or (default_item_tag if mode == "replace" or len(block) == 0 else _local_name(block[0]))
        identity_key, identity_value = _item_identity(item)
        target = None
        if mode == "merge" and identity_key and identity_value:
            for child in block:
                node_key, node_value = _node_identity(child)
                if node_key == identity_key and node_value == identity_value:
                    target = child
                    break
        if target is None:
            target = ET.SubElement(block, _tag(root, item_tag))
            added += 1
        else:
            updated += 1
        syntax_error = _apply_item_to_node(target, item, f"{block_name}[{index}]")
        if syntax_error:
            return syntax_error
    return updated, added


def _iter_mslx_files(folder_path: str, recursive: bool = True):
    if not folder_path or not os.path.exists(folder_path):
        return
    if recursive:
        for current_root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.lower().endswith(".mslx"):
                    yield os.path.join(current_root, filename)
    else:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(".mslx"):
                yield file_path


def _parse_xml_file(file_path: str):
    try:
        tree = ET.parse(file_path)
        return tree, tree.getroot(), None
    except Exception as exc:
        return None, None, str(exc)


def _operation_display_name(file_path: str, root=None) -> str:
    if root is not None and root.attrib.get("name"):
        return root.attrib.get("name")
    return os.path.splitext(os.path.basename(file_path))[0]


def _find_document_root(path: str) -> str:
    current = os.path.abspath(path)
    if os.path.isfile(current):
        current = os.path.dirname(current)
    while True:
        if os.path.isdir(os.path.join(current, "Operations")) and os.path.isdir(os.path.join(current, "DocumentTypes")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return ""
        current = parent


def _build_operation_index(document_root_path: str) -> dict:
    index = {}
    search_roots = [
        os.path.join(document_root_path, "DocumentTypes"),
        os.path.join(document_root_path, "Operations"),
    ]
    for search_root in search_roots:
        for file_path in _iter_mslx_files(search_root, recursive=True) or []:
            _, root, error = _parse_xml_file(file_path)
            if error:
                continue
            names = {
                os.path.splitext(os.path.basename(file_path))[0],
                _operation_display_name(file_path, root),
            }
            for name in names:
                if name:
                    index.setdefault(name, file_path)
    return index


def _action_info(file_path: str, action) -> dict:
    info = {
        "file_path": file_path,
        "action_type": _local_name(action),
        "action_name": action.attrib.get("name", ""),
    }
    for key in ("operationName", "nextDirection", "yesDirection", "noDirection", "abortDirection"):
        if action.attrib.get(key) is not None:
            info[key] = action.attrib.get(key)
    return info


def _operation_actions_in_file(file_path: str) -> list:
    _, root, error = _parse_xml_file(file_path)
    if error:
        return []
    actions = _find_child(root, "Actions")
    if actions is None:
        return []
    return [_action_info(file_path, action) for action in actions.iter() if _local_name(action) == "OperationAction"]


def _trace_operation_file(file_path: str, operation_index: dict, depth: int, visited=None) -> dict:
    visited = set() if visited is None else visited
    abs_file_path = os.path.abspath(file_path)
    tree, root, error = _parse_xml_file(abs_file_path)
    if error:
        return {"file_path": abs_file_path, "error": error, "calls": []}

    operation_name = _operation_display_name(abs_file_path, root)
    node = {
        "operation_name": operation_name,
        "file_path": abs_file_path,
        "calls": [],
    }
    if abs_file_path in visited:
        node["cycle"] = True
        return node
    if depth <= 0:
        node["max_depth_reached"] = True
        return node

    visited.add(abs_file_path)
    actions = _find_child(root, "Actions")
    if actions is None:
        return node

    for action in actions.iter():
        if _local_name(action) != "OperationAction":
            continue
        operation_name_attr = action.attrib.get("operationName", "")
        target_file = operation_index.get(operation_name_attr)
        call = {
            "action_name": action.attrib.get("name", ""),
            "operation_name": operation_name_attr,
            "target_file_path": target_file,
        }
        if target_file:
            call["operation"] = _trace_operation_file(target_file, operation_index, depth - 1, set(visited))
        else:
            call["missing_target"] = True
        node["calls"].append(call)
    return node


def _find_document_type_files(document_root_path: str, document_type_name: str) -> list:
    document_types_root = os.path.join(document_root_path, "DocumentTypes")
    if not os.path.exists(document_types_root):
        return []

    candidates = []
    for entry in os.listdir(document_types_root):
        entry_path = os.path.join(document_types_root, entry)
        if os.path.isdir(entry_path) and entry.lower() == document_type_name.lower():
            candidates.extend(list(_iter_mslx_files(entry_path, recursive=True) or []))
    if candidates:
        return candidates

    normalized = document_type_name.lower()
    for file_path in _iter_mslx_files(document_types_root, recursive=True) or []:
        relative = os.path.relpath(file_path, document_types_root).lower()
        if normalized in relative:
            candidates.append(file_path)
            continue
        _, root, error = _parse_xml_file(file_path)
        if error:
            continue
        root_name = (root.attrib.get("name") or "").lower()
        doc_type_attr = (root.attrib.get("documentTypeName") or root.attrib.get("DocumentTypeName") or "").lower()
        if normalized in root_name or normalized in doc_type_attr:
            candidates.append(file_path)
    return candidates


def _entrypoint_graph(document_root_path: str, document_type_name: str, max_depth: int) -> dict:
    document_root = os.path.abspath(document_root_path)
    operation_index = _build_operation_index(document_root)
    entry_files = [os.path.abspath(path) for path in _find_document_type_files(document_root, document_type_name)]
    entrypoints = []
    for file_path in entry_files:
        for action in _operation_actions_in_file(file_path):
            operation_name = action.get("operationName", "")
            target_file = operation_index.get(operation_name)
            entrypoint = {
                "document_type_file_path": file_path,
                "action_name": action.get("action_name"),
                "operation_name": operation_name,
                "target_file_path": target_file,
            }
            if target_file:
                entrypoint["operation"] = _trace_operation_file(target_file, operation_index, max_depth, {file_path})
            else:
                entrypoint["missing_target"] = True
            entrypoints.append(entrypoint)
    return {
        "document_root_path": document_root,
        "document_type_name": document_type_name,
        "document_type_files": entry_files,
        "entrypoints": entrypoints,
    }


def _flatten_reachable_operations(graph: dict) -> list:
    result = []

    def walk_operation(operation, path):
        if not operation:
            return
        current_path = path + [
            {
                "operation_name": operation.get("operation_name"),
                "file_path": operation.get("file_path"),
            }
        ]
        result.append({"operation": operation, "path": current_path})
        for call in operation.get("calls", []):
            walk_operation(call.get("operation"), current_path + [{"call_action_name": call.get("action_name"), "operation_name": call.get("operation_name")}])

    for entrypoint in graph.get("entrypoints", []):
        start_path = [
            {
                "document_type_file_path": entrypoint.get("document_type_file_path"),
                "entry_action_name": entrypoint.get("action_name"),
                "operation_name": entrypoint.get("operation_name"),
            }
        ]
        walk_operation(entrypoint.get("operation"), start_path)
    return result


def _reachable_action_matches(graph: dict, target: str) -> list:
    matches = []
    target_lower = target.lower()
    for item in _flatten_reachable_operations(graph):
        operation = item["operation"]
        file_path = operation.get("file_path")
        if not file_path:
            continue
        _, root, error = _parse_xml_file(file_path)
        if error:
            continue
        actions = _find_child(root, "Actions")
        if actions is None:
            continue
        for action in actions.iter():
            action_type = _local_name(action)
            action_name = action.attrib.get("name", "")
            if action_type.lower() == target_lower or action_name.lower() == target_lower or target_lower in action_name.lower():
                matches.append(
                    {
                        "path": item["path"],
                        "action": _action_info(file_path, action),
                    }
                )
    return matches


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
def find_usages(folder_path: str, operation_name: str, include_document_types: bool = True) -> str:
    """
    Глобальный поиск зависимостей. Ищет все .mslx файлы в папке, 
    в которых вызывается указанная операция (operation_name).
    """
    try:
        usages = []
        search_roots = [folder_path]
        document_root = _find_document_root(folder_path)
        if include_document_types and document_root:
            for extra_root in (os.path.join(document_root, "Operations"), os.path.join(document_root, "DocumentTypes")):
                if os.path.exists(extra_root) and extra_root not in search_roots:
                    search_roots.append(extra_root)

        seen_files = set()
        for search_root in search_roots:
            for file_path in _iter_mslx_files(search_root, recursive=True) or []:
                abs_file_path = os.path.abspath(file_path)
                if abs_file_path in seen_files:
                    continue
                seen_files.add(abs_file_path)
                _, root, error = _parse_xml_file(abs_file_path)
                if error:
                    continue
                actions = _find_child(root, "Actions")
                if actions is None:
                    continue
                matched_actions = []
                for action in actions.iter():
                    if action.attrib.get("operationName") == operation_name:
                        matched_actions.append(
                            {
                                "action_name": action.attrib.get("name", ""),
                                "action_type": _local_name(action),
                            }
                        )
                if not matched_actions:
                    continue
                usages.append(
                    {
                        "file": os.path.basename(abs_file_path),
                        "file_path": abs_file_path,
                        "operation": _operation_display_name(abs_file_path, root),
                        "actions": matched_actions,
                    }
                )
                continue
                
        return json.dumps(
            {
                "operation": operation_name,
                "include_document_types": include_document_types,
                "used_in": usages,
                "blocked": len(usages) == 0,
                "message": "No usages found. Treat this as a blocker before editing the candidate operation." if len(usages) == 0 else "",
            },
            indent=2,
            ensure_ascii=False,
        )
    except Exception as e:
        return f"Ошибка поиска зависимостей: {str(e)}"


@mcp.tool()
def trace_document_entrypoint(document_root_path: str, document_type_name: str, max_depth: int = 10) -> str:
    """
    Возвращает цепочку операций от типа документа: DocumentType -> OperationAction -> вложенные OperationAction.
    document_root_path должен указывать на абсолютный путь к /Document.
    """
    try:
        graph = _entrypoint_graph(document_root_path, document_type_name, max(1, min(int(max_depth), 30)))
        graph["blocked"] = len(graph.get("document_type_files", [])) == 0 or len(graph.get("entrypoints", [])) == 0
        if len(graph.get("document_type_files", [])) == 0:
            graph["message"] = f"Document type files not found for '{document_type_name}'."
        elif len(graph.get("entrypoints", [])) == 0:
            graph["message"] = f"No OperationAction entrypoints found for document type '{document_type_name}'."
        return json.dumps(graph, indent=2, ensure_ascii=False)
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to trace document entrypoint: {str(e)}"})


@mcp.tool()
def trace_operation_calls(file_path: str, depth: int = 5, document_root_path: str = "") -> str:
    """
    Рекурсивно раскрывает все OperationAction в операции и строит граф вызовов.
    document_root_path опционален; если пустой, сервер попробует найти /Document по file_path.
    """
    try:
        document_root = document_root_path or _find_document_root(file_path)
        if not document_root:
            return _json_response({"ok": False, "error": "document_root_path is required when /Document cannot be inferred from file_path."})
        operation_index = _build_operation_index(document_root)
        graph = _trace_operation_file(file_path, operation_index, max(1, min(int(depth), 30)))
        return json.dumps(graph, indent=2, ensure_ascii=False)
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to trace operation calls: {str(e)}"})


@mcp.tool()
def find_reachable_actions(document_root_path: str, document_type_name: str, action_type: str, max_depth: int = 10) -> str:
    """
    Находит все достижимые узлы указанного типа действия из точки входа типа документа.
    Например, action_type='AcceptInDocumentAction' для поиска реальной записи товара.
    """
    try:
        graph = _entrypoint_graph(document_root_path, document_type_name, max(1, min(int(max_depth), 30)))
        matches = _reachable_action_matches(graph, action_type)
        return json.dumps(
            {
                "document_root_path": os.path.abspath(document_root_path),
                "document_type_name": document_type_name,
                "action_type": action_type,
                "matches": matches,
                "blocked": len(matches) == 0,
                "message": "No reachable actions found. Do not edit by name-only hypothesis." if len(matches) == 0 else "",
            },
            indent=2,
            ensure_ascii=False,
        )
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to find reachable actions: {str(e)}"})


@mcp.tool()
def explain_call_path_to_action(document_root_path: str, document_type_name: str, target_action_type_or_name: str, max_depth: int = 10) -> str:
    """
    Объясняет путь от типа документа до достижимого действия по типу или имени узла.
    Возвращает человекочитаемые path_lines и структурированные matches.
    """
    try:
        graph = _entrypoint_graph(document_root_path, document_type_name, max(1, min(int(max_depth), 30)))
        matches = _reachable_action_matches(graph, target_action_type_or_name)
        path_lines = []
        for match in matches:
            lines = []
            for step in match.get("path", []):
                if step.get("document_type_file_path"):
                    lines.append(step["document_type_file_path"])
                elif step.get("call_action_name"):
                    lines.append(f" -> {step.get('call_action_name')} -> {step.get('operation_name')}")
                elif step.get("operation_name"):
                    lines.append(f" -> {step.get('operation_name')} ({step.get('file_path')})")
            action = match.get("action", {})
            lines.append(f" -> {action.get('action_type')} \"{action.get('action_name')}\" ({action.get('file_path')})")
            path_lines.append("\n".join(lines))

        return json.dumps(
            {
                "document_root_path": os.path.abspath(document_root_path),
                "document_type_name": document_type_name,
                "target_action_type_or_name": target_action_type_or_name,
                "path_lines": path_lines,
                "matches": matches,
                "blocked": len(matches) == 0,
                "message": "No call path found. This is a blocker before editing the candidate operation." if len(matches) == 0 else "",
            },
            indent=2,
            ensure_ascii=False,
        )
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to explain call path: {str(e)}"})

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
def validate_mslx_syntax(source: str, mode: str = "expression", normalize_braces: bool = True) -> str:
    """
    Проверяет синтаксис Mobile SMARTS через родной Cleverence.Parsing.dll.
    mode: expression, template, code или auto.
    """
    return _json_response(_run_syntax_checker(mode, source, normalize_braces))


@mcp.tool()
def copy_operation_file(source_file_path: str, target_file_path: str, new_operation_name: str = "", overwrite: bool = False) -> str:
    """
    Копирует .mslx операцию в новый файл и при необходимости меняет корневой атрибут name.
    source_file_path и target_file_path должны быть абсолютными путями.
    """
    try:
        if not os.path.isabs(source_file_path) or not os.path.isabs(target_file_path):
            return _json_response({"ok": False, "error": "source_file_path and target_file_path must be absolute paths."})
        if not os.path.exists(source_file_path):
            return _json_response({"ok": False, "error": f"Source file not found: {source_file_path}"})
        if os.path.exists(target_file_path) and not overwrite:
            return _json_response({"ok": False, "error": f"Target file already exists: {target_file_path}", "hint": "Pass overwrite=true only when replacing this file is intentional."})

        target_dir = os.path.dirname(target_file_path)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir)

        shutil.copy2(source_file_path, target_file_path)

        tree = ET.parse(target_file_path)
        root = tree.getroot()
        operation_name = new_operation_name.strip() if new_operation_name else os.path.splitext(os.path.basename(target_file_path))[0]
        if operation_name:
            root.set("name", operation_name)
            tree.write(target_file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

        return _json_response(
            {
                "ok": True,
                "source_file_path": source_file_path,
                "target_file_path": target_file_path,
                "operation_name": root.attrib.get("name"),
            }
        )
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to copy operation file: {str(e)}"})


@mcp.tool()
def update_operation_root_attributes(file_path: str, attributes_json: str) -> str:
    """
    Обновляет атрибуты корневого узла операции/типа документа.
    attributes_json - JSON-строка с объектом атрибутов, например '{"name":"ds_NewOperation"}'.
    """
    try:
        updates = _load_json_object(attributes_json, "attributes_json")
        for key, value in updates.items():
            mode = _syntax_mode_for_attribute(key)
            if mode:
                syntax_error = _validate_or_error(mode, str(value), f"update_operation_root_attributes:{key}")
                if syntax_error:
                    return syntax_error

        tree = ET.parse(file_path)
        root = tree.getroot()
        for key, value in updates.items():
            root.set(key, str(value))
        tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
        return _json_response({"ok": True, "file_path": file_path, "updated_attributes": updates})
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to update root attributes: {str(e)}"})


@mcp.tool()
def add_document_type_column(file_path: str, column_name: str, attributes_json: str = "{}") -> str:
    """
    Добавляет колонку в секцию <Columns> типа документа.
    attributes_json - JSON-строка с атрибутами колонки; если name/fieldName не переданы, будет добавлен name=column_name.
    """
    try:
        attrs = _load_json_object(attributes_json, "attributes_json")
        if not column_name and not attrs.get("name") and not attrs.get("fieldName"):
            return _json_response({"ok": False, "error": "column_name is required when attributes_json has neither name nor fieldName."})

        tree = ET.parse(file_path)
        root = tree.getroot()
        document_type = root if _local_name(root) == "DocumentType" else _find_child(root, "DocumentType")
        if document_type is None:
            return _json_response({"ok": False, "error": "DocumentType node not found."})

        columns = _find_child(document_type, "Columns")
        if columns is None:
            columns = ET.SubElement(document_type, _tag(root, "Columns"))

        name_attr = "fieldName" if any("fieldName" in child.attrib for child in columns) else "name"
        effective_name = attrs.get("name") or attrs.get("fieldName") or column_name
        for column in columns:
            if column.attrib.get("name") == effective_name or column.attrib.get("fieldName") == effective_name:
                return _json_response({"ok": False, "error": f"Column already exists: {effective_name}"})

        item_tag = _local_name(columns[0]) if len(columns) > 0 else "Column"
        column = ET.SubElement(columns, _tag(root, item_tag))
        if "name" not in attrs and "fieldName" not in attrs:
            attrs[name_attr] = column_name
        for key, value in attrs.items():
            column.set(key, str(value))

        tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
        return _json_response({"ok": True, "file_path": file_path, "column": dict(column.attrib)})
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to add document type column: {str(e)}"})


@mcp.tool()
def update_comparing_field_names_for_current_items(
    file_path: str,
    action_name: str,
    field_names_json: str,
    mode: str = "merge",
    item_tag: str = "",
) -> str:
    """
    Создает или обновляет вложенный список ComparingFieldNamesForCurrentItems у AcceptInDocumentAction.
    field_names_json принимает JSON-строку: массив строк, массив объектов, объект {"items":[...]}, либо map.
    mode: merge или replace. item_tag опционален; если пустой, используется существующий тег элемента или Value.
    """
    try:
        normalized_mode = (mode or "merge").strip().lower()
        if normalized_mode not in ("merge", "replace"):
            return _json_response({"ok": False, "error": "mode must be 'merge' or 'replace'."})

        field_names = _load_string_items(field_names_json, "field_names_json")

        tree = ET.parse(file_path)
        root = tree.getroot()
        action = _find_action(root, action_name)
        if action is None:
            return _json_response({"ok": False, "error": f"Action not found: {action_name}"})
        if _local_name(action) != "AcceptInDocumentAction":
            return _json_response({"ok": False, "error": f"Action '{action_name}' is {_local_name(action)}, expected AcceptInDocumentAction."})

        list_node = _find_child(action, "ComparingFieldNamesForCurrentItems")
        if list_node is None:
            list_node = ET.SubElement(action, _tag(root, "ComparingFieldNamesForCurrentItems"))

        existing_item_tag = _local_name(list_node[0]) if len(list_node) > 0 else ""
        effective_item_tag = item_tag.strip() or existing_item_tag or "Value"

        if normalized_mode == "replace":
            for child in list(list_node):
                list_node.remove(child)

        existing_values = {_node_string_value(child) for child in list_node if _node_string_value(child)}
        added = 0
        skipped = 0
        for field_name in field_names:
            clean_name = str(field_name).strip()
            if not clean_name:
                skipped += 1
                continue
            if normalized_mode == "merge" and clean_name in existing_values:
                skipped += 1
                continue
            child = ET.SubElement(list_node, _tag(root, effective_item_tag))
            child.text = clean_name
            existing_values.add(clean_name)
            added += 1

        tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
        return _json_response(
            {
                "ok": True,
                "file_path": file_path,
                "action_name": action_name,
                "mode": normalized_mode,
                "list_name": "ComparingFieldNamesForCurrentItems",
                "item_tag": effective_item_tag,
                "added": added,
                "skipped": skipped,
                "field_names": [_node_string_value(child) for child in list_node],
            }
        )
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to update ComparingFieldNamesForCurrentItems: {str(e)}"})


@mcp.tool()
def update_operation_action_io(
    file_path: str,
    action_name: str,
    in_keys_json: str = "[]",
    out_keys_json: str = "[]",
    out_values_json: str = "[]",
    mode: str = "merge",
) -> str:
    """
    Создает или обновляет вложенные секции InKeys, OutKeys и OutValues внутри OperationAction.
    *_json принимает JSON-строку: массив объектов, объект {"items":[...]}, либо map name -> value/object.
    mode: merge или replace.
    """
    try:
        normalized_mode = (mode or "merge").strip().lower()
        if normalized_mode not in ("merge", "replace"):
            return _json_response({"ok": False, "error": "mode must be 'merge' or 'replace'."})

        tree = ET.parse(file_path)
        root = tree.getroot()
        action = _find_action(root, action_name)
        if action is None:
            return _json_response({"ok": False, "error": f"Action not found: {action_name}"})
        if _local_name(action) != "OperationAction":
            return _json_response({"ok": False, "error": f"Action '{action_name}' is {_local_name(action)}, expected OperationAction."})

        stats = {}
        for block_name, raw_json, default_tag in (
            ("InKeys", in_keys_json, "Key"),
            ("OutKeys", out_keys_json, "Key"),
            ("OutValues", out_values_json, "Value"),
        ):
            result = _upsert_block_items(root, action, block_name, raw_json, default_tag, normalized_mode)
            if isinstance(result, str):
                return result
            updated, added = result
            stats[block_name] = {"updated": updated, "added": added}

        tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
        return _json_response({"ok": True, "file_path": file_path, "action_name": action_name, "mode": normalized_mode, "stats": stats})
    except Exception as e:
        return _json_response({"ok": False, "error": f"Failed to update OperationAction IO: {str(e)}"})

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
                    syntax_error = _validate_or_error("expression", new_code, f"update_action_code:{action_name}.expression")
                    if syntax_error:
                        return syntax_error
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
        for key, val_str in updates.items():
            syntax_error = _validate_or_error("auto", str(val_str), f"update_in_values:{action_name}.{key}")
            if syntax_error:
                return syntax_error
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
        for key, value in attrs.items():
            mode = _syntax_mode_for_attribute(key)
            if mode:
                syntax_error = _validate_or_error(mode, str(value), f"add_action_node:{action_name}.{key}")
                if syntax_error:
                    return syntax_error
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
        for key, value in updates.items():
            mode = _syntax_mode_for_attribute(key)
            if mode:
                syntax_error = _validate_or_error(mode, str(value), f"update_node_attributes:{action_name}.{key}")
                if syntax_error:
                    return syntax_error
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
def semantic_search_syntax(query: str, n_results: int, source_type: str = "all") -> str:
    """
    RAG-поиск: ищет информацию и примеры кода в базе знаний MobileSmarts (Qdrant).
    source_type: all, code или official. Фильтр работает по metadata.source_type,
    который записывает индексатор web_rag.py.
    """
    try:
        import os
        import requests
        import json
        from qdrant_client import QdrantClient
        from qdrant_client.http import models as qdrant_models

        safe_query = query[:1000]
        safe_limit = max(1, min(int(n_results), 20))
        source_filter = (source_type or "all").strip().lower()
        source_type_map = {
            "all": None,
            "any": None,
            "*": None,
            "code": ["code", "Исходный код проекта"],
            "project": ["code", "Исходный код проекта"],
            "source": ["code", "Исходный код проекта"],
            "код": ["code", "Исходный код проекта"],
            "official": ["official", "Официальная документация"],
            "docs": ["official", "Официальная документация"],
            "documentation": ["official", "Официальная документация"],
            "официальная": ["official", "Официальная документация"],
            "документация": ["official", "Официальная документация"],
        }

        if source_filter not in source_type_map:
            return json.dumps(
                {
                    "ok": False,
                    "error": "Недопустимый source_type. Используйте all, code или official.",
                    "source_type": source_type,
                    "allowed": ["all", "code", "official"],
                },
                indent=2,
                ensure_ascii=False,
            )

        qdrant_filter = None
        expected_source_type = source_type_map[source_filter]
        if expected_source_type:
            qdrant_filter = qdrant_models.Filter(
                must=[
                    qdrant_models.FieldCondition(
                        key="metadata.source_type",
                        match=qdrant_models.MatchAny(any=expected_source_type),
                    )
                ]
            )

        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

        if OPENROUTER_API_KEY:
            api_url = "https://openrouter.ai/api/v1/embeddings"
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "baai/bge-m3",
                "input": safe_query,
            }

            response = requests.post(api_url, headers=headers, json=payload, timeout=15)

            if response.status_code != 200:
                return f"Ошибка OpenRouter API: {response.text}"

            query_vector = response.json().get("data", [])[0].get("embedding")

        else:
            embed_model = "bge-m3"
            ollama_url = "http://localhost:11434/api/embeddings"

            response = requests.post(
                ollama_url,
                json={"model": embed_model, "prompt": safe_query},
                timeout=15,
            )

            if response.status_code != 200:
                return f"Ошибка локальной Ollama: {response.text}"

            query_vector = response.json().get("embedding")

        if not query_vector:
            return "Ошибка: модель вернула пустой вектор."

        client = QdrantClient(url="http://localhost:6333")
        search_response = client.query_points(
            collection_name="mobilesmarts_knowledge",
            query=query_vector,
            query_filter=qdrant_filter,
            limit=safe_limit,
            with_payload=True,
        )

        if not search_response.points:
            return json.dumps(
                {
                    "ok": True,
                    "query": safe_query,
                    "source_type": source_filter,
                    "results": [],
                    "message": "Ничего не найдено.",
                },
                indent=2,
                ensure_ascii=False,
            )

        formatted_results = []
        for hit in search_response.points:
            content = hit.payload.get("page_content", "")
            metadata = hit.payload.get("metadata", {})
            source_path = metadata.get("source", "Unknown")
            source_name = source_path.replace("\\", "/").split("/")[-1]

            formatted_results.append(
                {
                    "source_file": source_name,
                    "source_path": source_path,
                    "source_type": metadata.get("source_type"),
                    "source_label": metadata.get("source_label"),
                    "folder": metadata.get("folder"),
                    "relevance_score": round(hit.score, 3),
                    "content": content,
                }
            )

        return json.dumps(
            {
                "ok": True,
                "query": safe_query,
                "source_type": source_filter,
                "results": formatted_results,
            },
            indent=2,
            ensure_ascii=False,
        )

    except requests.exceptions.Timeout:
        return "Ошибка: превышено время ожидания векторизатора."
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
