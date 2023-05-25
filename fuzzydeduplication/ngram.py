from typing import List, Dict, Hashable, Any, Callable, Tuple
from uuid import uuid4
from copy import deepcopy
from fuzzydeduplication.duplicates_eliminator import DuplicatesEliminator

unique_ngram_key_name = '__unique_ngram_id__'

def n_grams(string, n):
  return [string[i:i + n] for i in range(len(string) - n + 1)]


def dice_coefficient(set1: set, set2: set):
  intersection = set1.intersection(set2)
  return 2 * len(intersection) / (len(set1) + len(set2))

class NGramm(DuplicatesEliminator):
  def __init__(self, 
    data: List[Dict[Hashable, Any]], 
    to_str: Callable[[Dict[Hashable, Any]], str], 
    n: int = 3,
  ) -> None:
    super().__init__(data)
    self.to_str = to_str
    self.n = n

    self.n_gram_sets = [set(n_grams(to_str(d), n)) for d in self.data]
    self.inverted_index: Dict[str, List[int]] = {}

    for idx, n_gram_set in enumerate(self.n_gram_sets):
      for n_gram in n_gram_set:
        if n_gram not in self.inverted_index:
          self.inverted_index[n_gram] = []
        self.inverted_index[n_gram].append(idx)

    for i in range(len(self.data)):
      self.data[i][unique_ngram_key_name] = str(uuid4())

  def query(self, target: Dict[Hashable, Any], threshold: float = 0.85) -> List[Dict[Hashable, Any]]:
    target_n_grams = set(n_grams(self.to_str(target), self.n))
    scores = [0.] * len(self.data)
    for n_gram in target_n_grams:
      if n_gram in self.inverted_index:
        for idx in self.inverted_index[n_gram]:
          scores[idx] = dice_coefficient(self.n_gram_sets[idx], target_n_grams)

    matches = [self.data[idx] for idx, score in enumerate(scores) if score >= threshold]

    return matches
  
  def find_duplicates(self, threshold: float = 0.85) -> List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]]:
    found_records = [False for _ in range(len(self.data))]
    inverted_idx: Dict[str, int] = {}
    res: List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]] = []
    cnt = 0

    for i in range(len(self.data)):
      inverted_idx[self.data[i][unique_ngram_key_name]] = i

    for d in self.data:
      if found_records[inverted_idx[d[unique_ngram_key_name]]]:
        continue
      
      found_records[inverted_idx[d[unique_ngram_key_name]]] = True

      qs = self.query(d, threshold)
      cnt += 1

      for q in qs:
        if q[unique_ngram_key_name] == d[unique_ngram_key_name]:
          continue
        res.append((d, q))
        found_records[inverted_idx[q[unique_ngram_key_name]]] = True

    self.cnt = cnt

    return res
