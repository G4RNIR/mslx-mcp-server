import xml.etree.ElementTree as ET
import re
import os
from pathlib import Path

def clean_mslx_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&#xD;&#xA;', ' ').replace('\r', ' ').replace('\n', ' ')
    return re.sub(r'\s+', ' ', text).strip()

def parse_mslx_to_markdown(file_path: str) -> str:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        return f"Ошибка парсинга XML файла: {e}"

    extracted_lines = []
    op_name = root.attrib.get("name", "Неизвестная_Операция")
    file_name = Path(file_path).name  # Получаем имя исходного файла
    
    # === ДОБАВЛЕНА ШАПКА МЕТАДАННЫХ ДЛЯ RAG ===
    extracted_lines.append("Тип_источника: Исходный код проекта")
    extracted_lines.append(f"Файл: {file_name}")
    extracted_lines.append(f"{'='*40}\n")
    # ==========================================

    extracted_lines.append(f"# Полное описание операции: {op_name}\n")
    
    # Превращаем дерево в список, чтобы парсер мог "заглядывать вперед"
    elements = list(root.iter())
    
    def get_next_action_identifier(start_idx):
        # Ищем следующий исполняемый блок в XML-дереве
        for j in range(start_idx + 1, len(elements)):
            next_tag = elements[j].tag.split('}')[-1]
            if next_tag.endswith("Action"):
                next_name = elements[j].attrib.get("name", "")
                next_id = elements[j].attrib.get("id", "")
                # Отдаем имя, а если его нет — системный ID
                return next_name if next_name else next_id
        return "Конец операции (return)"

    for i, elem in enumerate(elements):
        tag = elem.tag.split('}')[-1] 
        
        # 1. Извлечение глобальных переменных
        if tag in ["FieldInfo", "ReturnFieldInfo"]:
            fname = elem.attrib.get("fieldName", "")
            ftype = elem.attrib.get("fieldType", "")
            comment = elem.attrib.get("comment", "")
            line = f"- Переменная: **{fname}** (Тип: {ftype})"
            if comment: line += f" // *{comment}*"
            extracted_lines.append(line)
            continue
            
        # 2. Извлечение кнопок и горячих клавиш
        if tag == "KeyToAction":
            key = elem.attrib.get("key", "Кнопка")
            action = elem.attrib.get("action", "")
            alias = elem.attrib.get("alias", "")
            if action:
                btn_name = alias if alias else key
                extracted_lines.append(f"  🔘 **Кнопка/Действие на экране:** `{btn_name}` -> Переход на: `{action}`")
            continue

        # Обработка только основных блоков Action
        if not tag.endswith("Action"):
            continue

        name = elem.attrib.get("name", "")
        node_id = elem.attrib.get("id", "")  
        comment = elem.attrib.get("comment", "")
        
        # МАГИЯ ЗДЕСЬ: Узнаем, кто идет следующим в коде
        implicit_next = get_next_action_identifier(i)

        parts = [f"## Блок: {tag} (Операция: {op_name})"]
        
        if name: parts.append(f"**Имя шага:** {name}")
        if node_id: parts.append(f"**Внутренний ID:** `{node_id}`")
        if comment: parts.append(f"**Описание:** {comment}")
        
        # Специфичная логика
        if tag == "AssignAction":
            expr = elem.attrib.get("expression", "")
            if expr: parts.append(f"**Код:**\n```csharp\n{expr.strip()}\n```")
            
        elif tag == "ConditionAction":
            expr = elem.attrib.get("expression", "")
            yes_dir = elem.attrib.get("yesDirection", "")
            no_dir = elem.attrib.get("noDirection", "")
            
            # Если переход пустой — он идет на следующий блок по умолчанию
            actual_yes = yes_dir if yes_dir else implicit_next
            actual_no = no_dir if no_dir else implicit_next
            
            if expr: parts.append(f"**Условие:** `{expr.strip()}`")
            parts.append(f"**Если Истина -> Переход на:** {actual_yes}")
            parts.append(f"**Если Ложь -> Переход на:** {actual_no}")
            
        elif tag == "OperationAction":
            op_call = elem.attrib.get("operationName", "")
            if op_call: parts.append(f"**Вызов подпрограммы:** {op_call}")
            
        elif tag == "ForeachAction":
            items = elem.attrib.get("items", "")
            if items: parts.append(f"**Цикл (Foreach) по коллекции:** `{items}`")
            
        elif tag in ["SelectDocumentLineAction", "SelectDocumentLinesAction"]:
            sess_var = elem.attrib.get("sessionVariable", "")
            if sess_var: parts.append(f"**Результат поиска сохранить в:** `{sess_var}`")
            for child in elem:
                if child.tag.endswith("Query"):
                    where_expr = child.attrib.get("whereExpression", "")
                    if where_expr: parts.append(f"**Условие поиска БД (Where):** `{where_expr}`")
                    
        elif tag in ["BaloonAction", "QuestionYesNoAction", "FieldEditAction", "SimpleQuantityAction", "ScanAction"]:
            text = elem.attrib.get("text", "") or elem.attrib.get("message", "") or elem.attrib.get("welcomeText", "")
            clean_text = clean_mslx_html(text)
            if clean_text: parts.append(f"**Текст на экране ТСД:** {clean_text}")

        # МАРШРУТИЗАЦИЯ ПО УМОЛЧАНИЮ (Для всех, кроме условий)
        if tag != "ConditionAction":
            next_dir = elem.attrib.get("nextDirection", "")
            actual_next = next_dir if next_dir else implicit_next
            parts.append(f"**Следующий шаг -> Переход на:** {actual_next}")

        if len(parts) > 1:
            extracted_lines.append("\n".join(parts) + "\n")

    return "\n".join(extracted_lines)

if __name__ == "__main__":
    import sys
    
    # Если запустили двойным кликом (без аргументов)
    if len(sys.argv) == 1:
        print("Запуск в интерактивном режиме...")
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            
            print("Выберите директорию с файлами базы MobileSmarts (.mslx) в открывшемся диалоговом окне...")
            user_input_dir = filedialog.askdirectory(title="Выберите директорию с файлами .mslx")
            if not user_input_dir:
                print("Отмена операции. Директория не выбрана.")
                sys.exit(0)
                
        except ImportError:
            user_input_dir = input("Введите путь к директории с файлами базы MobileSmarts (.mslx): ").strip()
            while not user_input_dir:
                print("Путь не может быть пустым.")
                user_input_dir = input("Введите путь к директории с файлами базы MobileSmarts (.mslx): ").strip()
    else:
        # Если скрипт запустили с аргументом (например: python normalize.py "C:\Base")
        user_input_dir = sys.argv[1].strip()
    
    # Убираем кавычки
    user_input_dir = user_input_dir.strip('"').strip("'")
    target_dir = Path(user_input_dir)
    
    if not target_dir.exists() or not target_dir.is_dir():
        print("Указанная директория не найдена!")
        exit(1)

    print(f"\nПоиск файлов .mslx в папке: {target_dir}")
    mslx_files = list(target_dir.rglob("*.mslx")) # Ищет во всех вложенных папках
    
    if not mslx_files:
        print("Файлы .mslx не найдены.")
    else:
        # === НОВАЯ ЛОГИКА СОХРАНЕНИЯ ===
        # Создаем новую папку внутри целевой директории
        output_folder = target_dir / "Cleaned_Markdown"
        
        # exist_ok=True означает, что скрипт не выдаст ошибку, если папка уже существует
        output_folder.mkdir(parents=True, exist_ok=True) 

        print(f"Найдено файлов: {len(mslx_files)}. Начинаю обработку...")
        print(f"Все результаты будут сохранены в: {output_folder}\n")
        
        for mslx_file in mslx_files:
            # Парсим файл
            markdown_content = parse_mslx_to_markdown(mslx_file)
            
            # Формируем путь для сохранения в НОВОЙ папке (берем только имя файла + .md)
            output_md_file = output_folder / f"{mslx_file.stem}.md"
            
            # Сохраняем файл
            with open(output_md_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
                
            print(f"Конвертирован: {mslx_file.name} -> {output_md_file.name}")
            
        print("\nКонвертация успешно завершена!")
        print(f"Ваши очищенные файлы лежат здесь: {output_folder}")