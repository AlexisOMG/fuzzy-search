from typing import Any, Callable, Dict, List, Tuple, Hashable
from copy import deepcopy
from duplicates_eliminator import DuplicatesEliminator
from uuid import uuid4

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

class SNM(DuplicatesEliminator):
  def __init__(self, 
    data: List[Dict[Hashable, Any]],
    key: Callable[[Dict[Hashable, Any]], str],
    similarity: Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], float],
    w: int = 3,
  ) -> None:
    super().__init__(data)
    self.key = key
    self.similarity = similarity
    self.w = w

  def find_duplicates(self, threshold: float = 0.85) -> List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]]:
    cnt = 0
    duplicate_pairs: List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]] = []

    self.data.sort(key=self.key)
    
    win = self.data[:self.w]

    i = 0

    while i < len(self.data)-1:
      j = 1
      while j < len(win):
        cnt += 1
        if self.similarity(win[0], win[j]) > threshold:
          duplicate_pairs.append((win[0], win[j]))
        j += 1

      win.pop(0)

      if len(win) < self.w and i + len(win) < len(self.data)-1:
        win.append(self.data[i+len(win)+1])
      else:
        while len(win) > self.w:
          win.pop()
      
      i += 1

    self.cnt = cnt
    
    return duplicate_pairs

