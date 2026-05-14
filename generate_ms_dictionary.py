import os
import re
from collections import defaultdict
import lxml.etree as ET

# Расширенные регулярные выражения для максимального охвата синтаксиса
PATTERNS = {
    "1. Global (Системные функции)": re.compile(r'(global::[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)'),
    "2. Session (Сессия и настройки)": re.compile(r'\b(session\.[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)*)\b'),
    "3. Document (Шапка документа)": re.compile(r'\b(Document\.[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)*)\b'),
    "4. Строки (SelectedLine / CurrentLine)": re.compile(r'\b((?:SelectedLine|CurrentLine|line)\.[a-zA-Z0-9_]+)\b'),
    "5. Интерфейс (ui)": re.compile(r'\b(ui\.[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)*)\b'),
    "6. Cleverence API (Специфичные классы)": re.compile(r'\b([a-zA-Z0-9_]*Cleverence[a-zA-Z0-9_\.]+)\b'),
    "7. Общие методы (Коллекции, Строки, Даты)": re.compile(r'\b([A-Z][a-zA-Z0-9_]+\.[A-Z][a-zA-Z0-9_]+)\b(?=\s*\()')
}

def generate_dictionary(target_folder: str, output_file: str):
    print(f"🔍 Начинаем глубокое сканирование: {target_folder}...")
    
    dictionary = defaultdict(lambda: defaultdict(list))
    files_scanned = 0
    snippets_found = 0
    
    for root_dir, _, files in os.walk(target_folder):
        for filename in files:
            if not filename.endswith(".mslx"):
                continue
                
            file_path = os.path.join(root_dir, filename)
            try:
                tree = ET.parse(file_path)
                root_node = tree.getroot()
                nsmap = root_node.nsmap
                
                # Ищем везде: expression, condition, items и текстовые значения внутри <Value>
                xpath_query = '//*[@expression] | //*[@condition] | //*[@items] | //*[local-name()="Value"]'
                
                for elem in root_node.xpath(xpath_query, namespaces=nsmap):
                    texts_to_check = []
                    
                    if elem.attrib.get('expression'): texts_to_check.append(elem.attrib.get('expression'))
                    if elem.attrib.get('condition'): texts_to_check.append(elem.attrib.get('condition'))
                    if elem.attrib.get('items'): texts_to_check.append(elem.attrib.get('items'))
                    if elem.text and elem.text.strip(): texts_to_check.append(elem.text)
                    
                    for text in texts_to_check:
                        clean_text = " ".join(text.replace('\n', ' ').replace('\r', '').split())
                        if not clean_text or len(clean_text) < 3: 
                            continue
                        
                        # Проверяем все паттерны
                        for category, pattern in PATTERNS.items():
                            matches = pattern.findall(clean_text)
                            for match in set(matches):
                                # Увеличили лимит до 5 примеров для каждого токена
                                if len(dictionary[category][match]) < 5:
                                    # Избегаем добавления полных дублей примеров
                                    if clean_text not in dictionary[category][match]:
                                        dictionary[category][match].append(clean_text)
                                        snippets_found += 1
                                
            except Exception as e:
                # Игнорируем битые XML, если они есть
                continue
            
            files_scanned += 1

    print(f"✅ Просканировано файлов: {files_scanned}")
    print(f"🧩 Найдено полезных фрагментов кода: {snippets_found}")
    write_markdown_dictionary(dictionary, output_file)

def write_markdown_dictionary(dictionary, output_file):
    print(f"📝 Сохранение расширенного словаря в: {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 📚 Расширенный словарь синтаксиса Mobile SMARTS\n\n")
        f.write("> **ВАЖНО ДЛЯ ИИ-АГЕНТА:** Этот файл содержит реально используемый синтаксис проприетарной платформы. При написании кода строго сверяйся с этими вызовами. Не выдумывай методы C#, используй только то, что есть здесь.\n\n")
        
        for category, tokens in sorted(dictionary.items()):
            if not tokens: continue
            
            f.write(f"## {category}\n\n")
            for token, examples in sorted(tokens.items()):
                f.write(f"### `{token}`\n")
                f.write("**Примеры из базы:**\n")
                for ex in examples:
                    # Если кусок кода слишком длинный, немного обрезаем его для читаемости, 
                    # оставляя контекст вызова
                    display_text = ex if len(ex) < 150 else ex[:147] + "..."
                    f.write(f"```csharp\n{display_text}\n```\n")
                f.write("\n")
                
    print(f"🚀 Готово! Объемный словарь успешно сгенерирован.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Генератор словаря синтаксиса Mobile SMARTS")
    parser.add_argument("--folder", type=str, required=True, help="Путь к папке Documents типовой конфигурации")
    parser.add_argument("--output", type=str, default="MobileSmarts_Syntax_Dictionary.md", help="Имя выходного Markdown файла")
    
    args = parser.parse_args()
    generate_dictionary(args.folder, args.output)