from typing import Any, Callable, Dict, List, Tuple, Hashable
from copy import deepcopy

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
    records: List[Dict[Hashable, Any]],
    key: Callable[[Dict[Hashable, Any]], str],
    similarity: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], float],
    window_size: int = 3,
    similarity_threshold: float = 0.85,
) -> List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]]:
    data = deepcopy(records)

    data.sort(key=key)
    
    # Поиск дубликатов
    duplicates = []
    for i in range(len(data) - window_size + 1):
        window_records = data[i : i + window_size]
        for j in range(len(window_records)):
            for k in range(j + 1, len(window_records)):
                sim = similarity(window_records[j], window_records[k])
                if sim >= similarity_threshold:
                    duplicates.append((window_records[j], window_records[k]))
    return duplicates

# data = [
#     {"id": 1, "name": "Alice", "zip": "12345"},
#     {"id": 2, "name": "Alisa", "zip": "12346"},
#     {"id": 3, "name": "Alec", "zip": "12345"},
#     {"id": 4, "name": "Bobby", "zip": "54322"},
#     {"id": 5, "name": "Alyce", "zip": "12347"},
# ]

# key_attributes = ["name", "zip"]
# window_size = 3
# similarity_threshold = 0.9

# duplicates = sorted_neighborhood(data, key_attributes, window_size, similarity_threshold)
# print("Найденные дубликаты:")
# for dup in duplicates:
#     print(dup[0], dup[1])
