from typing import Any, Callable, Dict, List, Tuple
import itertools
from distances.levenshtein import levenshtein_distance_memopt
from dm_soundex import daitch_mokotoff_encode

def generate_key(record: Dict[str, Any], key_attributes: List[str], encoding_fn: Callable) -> str:
    key = ""
    for attr in key_attributes:
        encoded_attr = encoding_fn(record[attr])
        key += encoded_attr
    return key

def similarity(s: str, t: str, distance_fn: Callable) -> float:
    distance = distance_fn(s, t)
    max_length = max(len(s), len(t))
    return 1 - distance / max_length

def sorted_neighborhood(
    data: List[Dict[str, Any]],
    key_attributes: List[str],
    window_size: int,
    similarity_threshold: float,
    encoding_fn: Callable = daitch_mokotoff_encode,
    distance_fn: Callable = levenshtein_distance_memopt,
) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    
    # Генерация ключей и сортировка
    for record in data:
        record["key"] = generate_key(record, key_attributes, encoding_fn)
    data.sort(key=lambda x: x["key"])
    
    # Поиск дубликатов
    duplicates = []
    for i in range(len(data) - window_size + 1):
        window_records = data[i : i + window_size]
        for j in range(len(window_records)):
            for k in range(j + 1, len(window_records)):
                sim = similarity(window_records[j]["key"], window_records[k]["key"], distance_fn)
                if sim >= similarity_threshold:
                    duplicates.append((window_records[j], window_records[k]))
        # for pair in itertools.combinations(window_records, 2):
        #     sim = similarity(pair[0]["key"], pair[1]["key"], distance_fn)
        #     if sim >= similarity_threshold:
        #         duplicates.append((pair[0], pair[1]))
    return duplicates

data = [
    {"id": 1, "name": "Alice", "zip": "12345"},
    {"id": 2, "name": "Alisa", "zip": "12346"},
    {"id": 3, "name": "Alec", "zip": "12345"},
    {"id": 4, "name": "Bobby", "zip": "54322"},
    {"id": 5, "name": "Alyce", "zip": "12347"},
]

key_attributes = ["name", "zip"]
window_size = 3
similarity_threshold = 0.9

duplicates = sorted_neighborhood(data, key_attributes, window_size, similarity_threshold)
print("Найденные дубликаты:")
for dup in duplicates:
    print(dup[0], dup[1])
