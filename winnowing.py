import hashlib
from typing import List, Tuple, Dict, Set, Hashable, Any, Callable
from distances.jaccard import jaccard_similarity
from copy import deepcopy
from uuid import uuid4

unique_winnowing_key_name = '__unique_winnowing_id__'

def remove_spaces(s: str):
  return s.replace(" ", "")

def n_grams(string: str, n: int) -> List[str]:
  string = remove_spaces(string)
  return [string[i:i + n] for i in range(len(string) - n + 1)]

def hash_n_gram(n_gram: str) -> int:
  return int(hashlib.sha1(n_gram.encode('utf-8')).hexdigest(), 16)

def fingerprints(r: Dict[Hashable, Any], to_str: Callable[[Dict[Hashable, Any]], str], k: int, w: int) -> Set[int]:
  # Step 1: Generate k-grams
  k_grams = n_grams(to_str(r), k)

  # Step 2: Hash k-grams
  k_gram_hashes = [hash_n_gram(k_gram) for k_gram in k_grams]

  # Step 3: Generate min-hashes for each window
  fingerprints: Set[int] = set()
  prev_min_idx = -1
  for i in range(len(k_gram_hashes) - w + 1):
    window = k_gram_hashes[i:i + w]
    min_idx, min_hash = min(enumerate(window), key=lambda x: x[1])
    min_idx += i
    if min_idx != prev_min_idx:
      fingerprints.add(min_hash)
      prev_min_idx = min_idx

  return fingerprints



def winnowing_similarity(r1: Dict[Hashable, Any], r2: Dict[Hashable, Any], to_str: Callable[[Dict[Hashable, Any]], str], k: int = 5, w: int = 3) -> float:
  fingerprints1 = fingerprints(r1, to_str, k, w)
  fingerprints2 = fingerprints(r2, to_str, k, w)

  return jaccard_similarity(fingerprints1, fingerprints2)

def dice_coefficient(set1: set, set2: set):
  intersection = set1.intersection(set2)
  return 2 * len(intersection) / (len(set1) + len(set2))

class Winnowing:
  def __init__(self, data: List[Dict[Hashable, Any]], to_str: Callable[[Dict[Hashable, Any]], str], k: int = 3, w: int = 3) -> None:
    self.data = deepcopy(data)
    self.to_str = to_str
    self.k = k
    self.w = w
    self.fingerprints = [fingerprints(d, self.to_str, self.k, self.w) for d in self.data]
    self.inverted_index: Dict[int, List[int]] = {}
    for idx, fingerprint_set in enumerate(self.fingerprints):
      for fingerprint in fingerprint_set:
        if fingerprint not in self.inverted_index:
          self.inverted_index[fingerprint] = []
        self.inverted_index[fingerprint].append(idx)
    for i in range(len(self.data)):
      self.data[i][unique_winnowing_key_name] = str(uuid4())

  def query(self, target: Dict[Hashable, Any], threshold: float = 0.85) -> List[Dict[Hashable, Any]]:
    target_n_grams = fingerprints(target, self.to_str, self.k, self.w)
    scores = [0.] * len(self.data)
    for n_gram in target_n_grams:
      if n_gram in self.inverted_index:
        for idx in self.inverted_index[n_gram]:
          scores[idx] = dice_coefficient(self.fingerprints[idx], target_n_grams)

    matches = [self.data[idx] for idx, score in enumerate(scores) if score >= threshold]

    return matches
  
  def find_duplicates(self, threshold: float = 0.85) -> List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]]:
    found_records = [False for _ in range(len(self.data))]
    inverted_idx: Dict[str, int] = {}
    res: List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]] = []

    for i in range(len(self.data)):
      inverted_idx[self.data[i][unique_winnowing_key_name]] = i

    for d in self.data:
      if found_records[inverted_idx[d[unique_winnowing_key_name]]]:
        continue
      
      found_records[inverted_idx[d[unique_winnowing_key_name]]] = True
      qs = self.query(d, threshold)

      for q in qs:
        if q[unique_winnowing_key_name] == d[unique_winnowing_key_name]:
          continue
        res.append((d, q))
        found_records[inverted_idx[q[unique_winnowing_key_name]]] = True

    return res

