import re
from typing import List, Tuple, Dict

from hashlib import md5

from distances.jaccard import jaccard_similarity as js

def compute_hashes(tokens: List[str]) -> List[int]:
    # Вычисление хеш-значений для токенов с использованием md5
    return [int(md5(token.encode('utf-8')).hexdigest(), 16) for token in tokens]


def create_fingerprints(hashes: List[int], window_size: int) -> List[int]:
    # Создание слепков
    fingerprints = []
    for i in range(len(hashes) - window_size + 1):
        window = hashes[i:i + window_size]
        min_hash = min(window)
        if not fingerprints or fingerprints[-1] != min_hash:
            fingerprints.append(min_hash)
    return fingerprints

def jaccard_similarity(fingerprints1: List[int], fingerprints2: List[int]) -> float:
    return js(set(fingerprints1), set(fingerprints2))

# def winnowing(text1: str, text2: str, window_size: int) -> float:
#     tokens1 = tokenize(text1)
#     tokens2 = tokenize(text2)

#     hashes1 = compute_hashes(tokens1)
#     hashes2 = compute_hashes(tokens2)

#     fingerprints1 = create_fingerprints(hashes1, window_size)
#     fingerprints2 = create_fingerprints(hashes2, window_size)

#     similarity = jaccard_similarity(fingerprints1, fingerprints2)
#     return similarity

def tokenize_record(record: Dict[str, str]) -> List[str]:
    # Токенизация записи, объединение значений полей
    tokens = []
    for field in record.values():
        field_tokens = re.findall(r'\w+', field.lower())
        tokens.extend(field_tokens)
    return tokens

def winnowing_records(record1: Dict[str, str], record2: Dict[str, str], window_size: int) -> float:
    tokens1 = tokenize_record(record1)
    tokens2 = tokenize_record(record2)

    hashes1 = compute_hashes(tokens1)
    hashes2 = compute_hashes(tokens2)

    fingerprints1 = create_fingerprints(hashes1, window_size)
    fingerprints2 = create_fingerprints(hashes2, window_size)

    similarity = jaccard_similarity(fingerprints1, fingerprints2)
    return similarity

record1 = {
    "name": "Иванов Иван Иванович",
    "address": "ул. Ленина, д. 5, кв. 3",
    "phone": "+7(123)456-78-90",
}

record2 = {
    "name": "Иванов Иван Иванович",
    "address": "ул. Ленина, дом 5, квартира 3",
    "phone": "8(123)456-78-90",
}

window_size = 2
similarity = winnowing_records(record1, record2, window_size)
print(f"Сходство между записями: {similarity:.2f}")