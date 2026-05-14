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
    extracted_lines.append(f"# Операция: {op_name}\n")
    
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] 
        
        if tag in ["FieldInfo", "ReturnFieldInfo"]:
            fname = elem.attrib.get("fieldName", "")
            ftype = elem.attrib.get("fieldType", "")
            comment = elem.attrib.get("comment", "")
            line = f"- Переменная: **{fname}** (Тип: {ftype})"
            if comment: line += f" // *{comment}*"
            extracted_lines.append(line)
            
        elif tag.endswith("Action"):
            name = elem.attrib.get("name", "")
            comment = elem.attrib.get("comment", "")
            
            if not name and not comment and tag not in ["AssignAction", "ConditionAction", "OperationAction"]:
                continue

            parts = [f"## Блок: {tag}"]
            if name: parts.append(f"**Имя шага:** {name}")
            if comment: parts.append(f"**Описание:** {comment}")
            
            if tag == "AssignAction":
                expr = elem.attrib.get("expression", "")
                if expr: parts.append(f"**Код:**\n```csharp\n{expr.strip()}\n```")
            elif tag == "ConditionAction":
                expr = elem.attrib.get("expression", "")
                yes_dir = elem.attrib.get("yesDirection", "")
                no_dir = elem.attrib.get("noDirection", "")
                if expr: parts.append(f"**Условие:** `{expr.strip()}`")
                if yes_dir: parts.append(f"**Если Истина:** {yes_dir}")
                if no_dir: parts.append(f"**Если Ложь:** {no_dir}")
            elif tag == "OperationAction":
                op_call = elem.attrib.get("operationName", "")
                if op_call: parts.append(f"**Вызов подпрограммы:** {op_call}")
            elif tag in ["BaloonAction", "QuestionYesNoAction", "FieldEditAction", "SimpleQuantityAction"]:
                text = elem.attrib.get("text", "") or elem.attrib.get("message", "") or elem.attrib.get("welcomeText", "")
                clean_text = clean_mslx_html(text)
                if clean_text: parts.append(f"**Текст пользователю:** {clean_text}")

            if len(parts) > 1:
                extracted_lines.append("\n".join(parts) + "\n")

    return "\n".join(extracted_lines)

if __name__ == "__main__":
    # Запрашиваем путь у пользователя
    user_input_dir = input("Введите путь к директории с файлами базы MobileSmarts (.mslx): ").strip()
    
    # Убираем кавычки, если пользователь вставил путь с кавычками (часто бывает в Windows)
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
        print(f"Найдено файлов: {len(mslx_files)}. Начинаю обработку...")
        
        for mslx_file in mslx_files:
            # Парсим файл
            markdown_content = parse_mslx_to_markdown(mslx_file)
            
            # Формируем путь для сохранения (тот же путь, но расширение .md)
            output_md_file = mslx_file.with_suffix('.md')
            
            # Сохраняем в той же папке
            with open(output_md_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
                
            print(f"Конвертирован: {mslx_file.name} -> {output_md_file.name}")
            
        print("\nКонвертация успешно завершена!")