import os
import lxml.etree as ET
import chromadb
import hashlib

def build_index(config_folder: str, db_path: str = "./mslx_vector_db"):
    print(f"🚀 Запуск индексации конфигурации из {config_folder}")
    print(f"📁 Векторная база будет сохранена в {db_path}")
    
    # Инициализация локальной векторной БД
    client = chromadb.PersistentClient(path=db_path)
    
    # Удаляем старую коллекцию, если она была, чтобы создать заново (полный реиндекс)
    try:
        client.delete_collection(name="mslx_syntax")
    except Exception:  # Теперь перехватывает любые ошибки отсутствия базы
        pass
        
    collection = client.create_collection(name="mslx_syntax")
    
    documents = []
    metadatas = []
    ids = []
    unique_hashes = set() # Для дедупликации одинакового кода
    
    for root_dir, _, files in os.walk(config_folder):
        for filename in files:
            if not filename.endswith(".mslx"): continue
            
            file_path = os.path.join(root_dir, filename)
            try:
                tree = ET.parse(file_path)
                root_node = tree.getroot()
                nsmap = root_node.nsmap
                
                # Ищем все куски кода в expression
                for elem in root_node.xpath('//*[@expression]', namespaces=nsmap):
                    expr = elem.attrib.get('expression', '').strip()
                    if len(expr) < 10: # Игнорируем слишком короткий код
                        continue
                        
                    # Создаем уникальный хэш сниппета
                    snippet_hash = hashlib.md5(expr.encode('utf-8')).hexdigest()
                    
                    if snippet_hash not in unique_hashes:
                        unique_hashes.add(snippet_hash)
                        documents.append(expr)
                        node_name = elem.attrib.get('name', elem.tag.split('}')[-1])
                        metadatas.append({"file": filename, "node": node_name})
                        ids.append(snippet_hash)
                        
            except Exception as e:
                continue
                
    # Загружаем пачками (batch) для скорости
    print(f"🧠 Найдено {len(documents)} уникальных фрагментов кода. Начинаем векторизацию (это может занять пару минут)...")
    
    batch_size = 500
    for i in range(0, len(documents), batch_size):
        collection.add(
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )
        print(f"   Проиндексировано {min(i+batch_size, len(documents))} / {len(documents)}")

    print("✅ Векторный индекс успешно создан!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, required=True, help="Путь к /Document")
    parser.add_argument("--db", type=str, default="./mslx_vector_db", help="Путь сохранения базы")
    args = parser.parse_args()
    build_index(args.folder, args.db)